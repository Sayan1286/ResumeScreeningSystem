import { useState } from "react";
import type { FormEvent } from "react";
import { apiRequest } from "./api";

interface CreateJobProps {
  onJobCreated: () => void;
}

function CreateJob({ onJobCreated }: CreateJobProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [requiredSkills, setRequiredSkills] = useState("");
  const [minExperience, setMinExperience] = useState(0);
  const [education, setEducation] = useState("");
  const [keywords, setKeywords] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await apiRequest("/jobs", {
        method: "POST",
        body: JSON.stringify({
          title,
          description,
          required_skills: requiredSkills,
          min_experience: minExperience,
          education: education || null,
          keywords: keywords || null,
        }),
      });

      setTitle("");
      setDescription("");
      setRequiredSkills("");
      setMinExperience(0);
      setEducation("");
      setKeywords("");

      onJobCreated();
    } catch {
      setError("Unable to create job.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="welcome-card create-job">
      <h2>Create New Job</h2>

    <form onSubmit={handleSubmit}>
  <div className="form-group">
    <label>Job Title</label>

    <input
      type="text"
      value={title}
      onChange={(event) => setTitle(event.target.value)}
      placeholder="e.g. Junior Data Analyst"
      required
    />
  </div>

  <div className="form-group">
    <label>Description</label>

    <textarea
      value={description}
      onChange={(event) => setDescription(event.target.value)}
      placeholder="Describe the job requirements..."
      required
    />
  </div>

  <div className="form-group">
    <label>Required Skills</label>

    <input
      type="text"
      value={requiredSkills}
      onChange={(event) =>
        setRequiredSkills(event.target.value)
      }
      placeholder="Python, MySQL, Excel"
      required
    />
  </div>

  <div className="form-group">
    <label>Minimum Experience (years)</label>

    <input
      type="number"
      min="0"
      value={minExperience}
      onChange={(event) =>
        setMinExperience(Number(event.target.value))
      }
    />
  </div>

  <div className="form-group">
    <label>Education</label>

    <input
      type="text"
      value={education}
      onChange={(event) => setEducation(event.target.value)}
      placeholder="B.Tech"
    />
  </div>

  <div className="form-group">
    <label>Keywords</label>

    <input
      type="text"
      value={keywords}
      onChange={(event) => setKeywords(event.target.value)}
      placeholder="Data Analysis, Database, Computer Science"
    />
  </div>

  {error && <p className="error">{error}</p>}

  <button type="submit" disabled={loading}>
    {loading ? "Creating Job..." : "Create Job"}
  </button>
  </form> 
    </section>
  );
}

export default CreateJob;