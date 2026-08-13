import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path


SAMPLE_RATE = 44100
CHANNELS = 1


def record_meeting():
    print("\n🎙️ MEETING RECORDING")
    print("=" * 50)
    print("Press ENTER to start recording...")
    input()

    print("\n🔴 Recording...")
    print("Press ENTER to stop recording.")

    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=callback
    ):
        input()

    print("⏹️ Recording stopped.")

    audio = __import__("numpy").concatenate(recording, axis=0)

    output_dir = Path("recordings")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "meeting.wav"

    write(str(output_file), SAMPLE_RATE, audio)

    print(f"✅ Audio saved: {output_file}")

    return str(output_file)