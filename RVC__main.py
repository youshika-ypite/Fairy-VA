import asyncio
import datetime
import os
import time

import edge_tts
import librosa
import torch

from gradio import processing_utils
from fairseq import checkpoint_utils
from rvc_config import Config
from lib.infer_pack.models import (
    SynthesizerTrnMs256NSFsid,
    SynthesizerTrnMs256NSFsid_nono,
    SynthesizerTrnMs768NSFsid,
    SynthesizerTrnMs768NSFsid_nono,
)
from rvc_rmvpe import RMVPE
from rvc_vc_infer_pipeline import VC

from configure__main import Configuration, Pathlib_y

limitation = os.getenv("SYSTEM") == "spaces"

config = Config()

edge_output_filename = "result/edge/edge_output.mp3"

model_root = "weights"

def search():
    models = [d for d in os.listdir(model_root) if os.path.isdir(os.path.join(model_root, d))]
    if len(models) == 0: raise ValueError("tts-out || No model found in `weights` folder")
    models.sort()
    Configuration.update_models(models)

    return models
models = search()

def model_data(model_name):
    pth_files = [
        os.path.join(model_root, model_name, f)
        for f in os.listdir(os.path.join(model_root, model_name))
        if f.endswith(".pth")
    ]
    if len(pth_files) == 0:
        raise ValueError(f"No pth file found in {model_root}/{model_name}")
    pth_path = pth_files[0]
    print(f"tts-out || Loading {pth_path}")
    cpt = torch.load(pth_path, map_location="cpu", weights_only=True)
    tgt_sr = cpt["config"][-1]
    cpt["config"][-3] = cpt["weight"]["emb_g.weight"].shape[0]  # n_spk
    if_f0 = cpt.get("f0", 1)
    version = cpt.get("version", "v1")
    if version == "v1":
        if if_f0 == 1:
            net_g = SynthesizerTrnMs256NSFsid(*cpt["config"], is_half=config.is_half)
        else:
            net_g = SynthesizerTrnMs256NSFsid_nono(*cpt["config"])
    elif version == "v2":
        if if_f0 == 1:
            net_g = SynthesizerTrnMs768NSFsid(*cpt["config"], is_half=config.is_half)
        else:
            net_g = SynthesizerTrnMs768NSFsid_nono(*cpt["config"])
    else:
        raise ValueError("tts-out || Unknown version")
    del net_g.enc_q
    net_g.load_state_dict(cpt["weight"], strict=False)
    print("tts-out || Model loaded")
    net_g.eval().to(config.device)
    if config.is_half:
        net_g = net_g.half()
    else:
        net_g = net_g.float()
    vc = VC(tgt_sr, config)

    index_files = [
        os.path.join(model_root, model_name, f)
        for f in os.listdir(os.path.join(model_root, model_name))
        if f.endswith(".index")
    ]
    if len(index_files) == 0:
        print("tts-out || No index file found")
        index_file = ""
    else:
        index_file = index_files[0]
        print(f"tts-out || Index file found: {index_file}")

    return tgt_sr, net_g, vc, version, index_file, if_f0

def load_hubert():
    global hubert_model
    models, _, _ = checkpoint_utils.load_model_ensemble_and_task(
        ["rvc_hubert_base.pt"],
        suffix="",
    )
    hubert_model = models[0]
    hubert_model = hubert_model.to(config.device)
    if config.is_half: hubert_model = hubert_model.half()
    else: hubert_model = hubert_model.float()
    return hubert_model.eval()

class generateTTS():
    def __init__(self):
        print("tts-out || ### RVC LOGGING")
        print("tts-out || Loading hubert model...")
        self.hubert_model = load_hubert()
        print("tts-out || Hubert model loaded.")
        print("tts-out || Loading rmvpe model...")
        self.rmvpe_model = RMVPE("rvc_rmvpe.pt", config.is_half, config.device)
        print("tts-out || rmvpe model loaded.")

    def load(self):

        print("tts-out || Loading RVC model...")
        models = search()
        if Configuration._ACTIVE() == 0: model = 0
        else: model = Configuration._ACTIVE()
        try: self.tgt_sr, self.net_g, self.vc, self.version, self.index_file, self.if_f0 = model_data(models[model])
        except Exception as exc:
            self.tgt_sr, self.net_g, self.vc, self.version, self.index_file, self.if_f0 = model_data(models[0])
            print("tts-out 124|| ", exc)
        print("tts-out || RVC model loaded.")

    def tts(
        self,
        tts_text,
        speed, tts_voice,
        f0_up_key, f0_method,
        index_rate, protect,
        filter_radius=3,
        resample_sr=0,
        rms_mix_rate=0.25
    ):
        model_name = Configuration._CONFIG()['settings']['models'][Configuration._CONFIG()['settings']['active']]
        print( "tts-out ||------------------||")
        print( "tts-out || ", datetime.datetime.now())
        print( "tts-out ||------------------||")
        print( "tts-out || tts_text:")
        print(f"tts-out || {tts_text}")
        print(f"tts-out || tts_voice: {tts_voice}")
        print(f"tts-out || Model name: {model_name}")
        print(f"tts-out || F0: {f0_method}, Key: {f0_up_key}, Index: {index_rate}, Protect: {protect}")
        print( "tts-out ||------------------||")
        try:
            if limitation and len(tts_text) > 280:
                print( "tts-out || ############### ERROR ###############")
                print( "tts-out || Error: Text too long")
                print(f"tts-out || Text characters should be at most 280 in this huggingface space, but got {len(tts_text)} characters.")
                return 0
            
            t0 = time.time()

            if speed >= 0: speed_str = f"+{speed}%"
            else: speed_str = f"{speed}%"
            try:
                asyncio.run(
                    edge_tts.Communicate(
                        tts_text, "-".join(tts_voice.split("-")[:-1]), rate=speed_str
                    ).save(edge_output_filename)
                )
            except Exception as exc: print("tts-out || ", exc)
            
            t1 = time.time()
            edge_time = t1 - t0
            
            audio, sr = librosa.load(edge_output_filename, sr=16000, mono=True)
            duration = len(audio) / sr

            print(f"tts-out || Audio duration: {duration}s")
            if limitation and duration >= 20:
                print( "tts-out || ############### ERROR ###############")
                print( "tts-out || Error: Audio too long")
                print(f"tts-out || Audio should be less than 20 seconds in this huggingface space, but got {duration}s.")
                return 0

            f0_up_key = int(f0_up_key)

            if not hubert_model: load_hubert()
            if f0_method == "rmvpe": self.vc.model_rmvpe = self.rmvpe_model

            times = [0, 0, 0]
            audio_opt = self.vc.pipeline(
                hubert_model,
                self.net_g, 0,
                audio,
                edge_output_filename,
                times,
                f0_up_key, f0_method,
                self.index_file, index_rate,
                self.if_f0,
                filter_radius,
                self.tgt_sr,
                resample_sr,
                rms_mix_rate,
                self.version,
                protect,
                None,
            )
            if self.tgt_sr != resample_sr >= 16000: self.tgt_sr = resample_sr

            filename = Pathlib_y.get_mainLOCALpath()+"/result.wav"
            os.remove(filename)
            processing_utils.audio_to_file(self.tgt_sr, audio_opt, filename, 'wav')

            print(f"tts-out || Success. Time: edge-tts: {edge_time}s, npy: {times[0]}s, f0: {times[1]}s, infer: {times[2]}s")        
        except EOFError: print("tts-out || It seems that the edge-tts output is not valid. LangError")