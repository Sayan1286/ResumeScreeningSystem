import { useState } from "react";
import { apiRequest } from "./api";

interface UploadResumeProps {
  jobId: number;
  onUploaded: () => void;
}

function UploadResume({
  jobId,
  onUploaded,
}: UploadResumeProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!file) {
      setError("Please select a resume.");
      return;
    }

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const formData = new FormData();

      formData.append("file", file);

      await apiRequest(
        `/resumes?job_id=${jobId}`,
        {
          method: "POST",
          headers: {},
          body: formData,
        },
      );

      setFile(null);
      setMessage("Resume uploaded successfully.");

      onUploaded();
    } catch {
      setError("Unable to upload resume.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="welcome-card upload-resume">
      <h2>Upload Resume</h2>

      <p>
        Upload a PDF or DOCX resume for the selected job.
      </p>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(event) => {
            setFile(event.target.files?.[0] ?? null);
          }}
        />

        {error && <p className="error">{error}</p>}

        {message && (
          <p className="success">{message}</p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Uploading..." : "Upload Resume"}
        </button>
      </form>
    </section>
  );
}

export default UploadResume;