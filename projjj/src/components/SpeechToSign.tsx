import { useState } from "react";
import axios from "axios";

const SpeechToSign = () => {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

interface UploadEvent extends React.ChangeEvent<HTMLInputElement> {}

const handleUpload = async (event: UploadEvent): Promise<void> => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("audio", file);

    try {
        const response = await axios.post<Blob>("http://127.0.0.1:8000/speech-to-sign/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob", // To receive the video file
        });

        const videoBlob = new Blob([response.data], { type: "video/mp4" });
        setVideoUrl(URL.createObjectURL(videoBlob));
    } catch (error) {
        console.error("Error processing audio:", error);
        alert("Error processing speech.");
    } finally {
        setLoading(false);
    }
};

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <h2 className="text-xl font-bold">Speech to Sign Language</h2>
      
      <input type="file" accept="audio/*" onChange={handleUpload} className="my-4" />

      {loading && <p className="text-gray-500">Processing...</p>}

      {videoUrl && (
        <video controls width="500" className="rounded-lg shadow-lg">
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
};

export default SpeechToSign;
