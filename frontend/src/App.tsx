import { useCallback, useEffect, useState } from "react";
import Login from "./Login";
import CreateJob from "./CreateJob";
import UploadResume from "./UploadResume";
import "./App.css";

const API_BASE_URL = "https://resumescreeningsystem-wpxz.onrender.com";
interface Job {
  id: number;
  recruiter_id: number | null;
  is_demo: boolean;
  title: string;
  description: string;
  required_skills: string;
  min_experience: number;
  education: string | null;
  keywords: string | null;
  created_at: string;
  updated_at: string;
}

interface ScreeningResult {
  rank: number;
  resume_id: number;
  candidate_id: number;
  candidate_name: string;
  candidate_email: string;
  original_filename: string;

  skill_score: number;
  experience_score: number;
  education_score: number;
  keyword_score: number;
  total_score: number;
  match_percentage: number;

  status: string;
  skills_explanation: string;
  experience_explanation: string;
  education_explanation: string;
  keywords_explanation: string;
  recommendation: string;
}

async function apiRequest(
  endpoint: string,
  options: RequestInit = {},
) {
 const token = localStorage.getItem("access_token");

  const headers = new Headers(options.headers);

  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = "Request failed";

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Ignore JSON parsing errors.
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function App() {
  const [loggedIn, setLoggedIn] = useState(
  Boolean(localStorage.getItem("access_token")),
);

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const [candidates, setCandidates] = useState<ScreeningResult[]>([]);

  const [loadingJobs, setLoadingJobs] = useState(false);
  const [loadingCandidates, setLoadingCandidates] = useState(false);

  const [error, setError] = useState("");

  const [selectedCandidate, setSelectedCandidate] =
    useState<ScreeningResult | null>(null);

  /*
   * Load candidates ONLY for the selected job.
   *
   * Changing the job does NOT upload anything.
   * It simply loads the resumes/results that already
   * belong to that job and current user.
   */
  const loadCandidates = useCallback(async (jobId: number) => {
    setLoadingCandidates(true);
    setError("");
    setSelectedCandidate(null);

    try {
      const data = await apiRequest(
        `/screening/jobs/${jobId}`,
      );

      setCandidates(data);
    } catch (err) {
      setCandidates([]);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load candidates",
      );
    } finally {
      setLoadingCandidates(false);
    }
  }, []);

  /*
   * Load all available jobs after login.
   *
   * Demo jobs are shared.
   * User-created jobs belong only to the current user.
   */
  const loadJobs = useCallback(async () => {
    setLoadingJobs(true);
    setError("");

    try {
      const data: Job[] = await apiRequest("/jobs");

      setJobs(data);

      /*
       * Select the first job only if there is no
       * currently selected job.
       *
       * We do NOT upload a resume here.
       */
      setSelectedJob((currentJob) => {
        if (currentJob) {
          const stillExists = data.find(
            (job) => job.id === currentJob.id,
          );

          return stillExists || data[0] || null;
        }

        return data[0] || null;
      });
    } catch (err) {
      setJobs([]);
      setSelectedJob(null);

      setError(
        err instanceof Error
          ? err.message
          : "Failed to load jobs",
      );
    } finally {
      setLoadingJobs(false);
    }
  }, []);

  /*
   * Load jobs once after the user logs in.
   */
  useEffect(() => {
    if (!loggedIn) {
      return;
    }

    loadJobs();
  }, [loggedIn, loadJobs]);

  /*
   * Whenever the selected job changes:
   *
   * 1. Load existing candidates for that job.
   * 2. DO NOT ask for a resume.
   * 3. DO NOT clear/delete existing resumes.
   * 4. DO NOT create a new upload.
   */
  useEffect(() => {
    if (!selectedJob) {
      setCandidates([]);
      return;
    }

    loadCandidates(selectedJob.id);
  }, [selectedJob, loadCandidates]);

  /*
   * Login success.
   */
  const handleLogin = () => {
    setLoggedIn(true);
  };

  /*
   * Logout.
   */
  const handleLogout = () => {
   localStorage.removeItem("access_token");

    setLoggedIn(false);
    setJobs([]);
    setSelectedJob(null);
    setCandidates([]);
    setSelectedCandidate(null);
    setError("");
  };

  /*
   * Called after a new job is created.
   *
   * Reload jobs and select the newly available list.
   */
  const handleJobCreated = async () => {
    await loadJobs();
  };

  /*
   * Resume upload completed.
   *
   * We refresh candidates for the CURRENT job only.
   * Changing jobs later does not require another upload.
   */
  const handleResumeUploaded = async () => {
    if (!selectedJob) {
      return;
    }

    await loadCandidates(selectedJob.id);
  };

  /*
   * Delete a resume/candidate.
   */
  const handleDeleteResume = async (resumeId: number) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this resume?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await apiRequest(`/resumes/${resumeId}`, {
        method: "DELETE",
      });

      if (selectedJob) {
        await loadCandidates(selectedJob.id);
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to delete resume",
      );
    }
  };

  if (!loggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  const demoJobs = jobs.filter((job) => job.is_demo);
  const myJobs = jobs.filter((job) => !job.is_demo);

  const averageScore =
    candidates.length > 0
      ? Math.round(
          candidates.reduce(
            (sum, candidate) => sum + candidate.total_score,
            0,
          ) / candidates.length,
        )
      : 0;

  return (
    <div className="app">
      {/* ================= HEADER ================= */}

      <header className="app-header">
        <div>
          <h1>Resume Screening System</h1>
          <p>AI-powered resume screening and candidate ranking</p>
        </div>

        <button
          type="button"
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>
      </header>

      <main className="app-content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* ================= JOB CREATION ================= */}

        <section className="card">
          <h2>Create Your Own Job</h2>

          <p className="section-description">
            Creating a job is optional. You can use any of the
            ready-made demo jobs below without creating anything.
          </p>

          <CreateJob onJobCreated={handleJobCreated} />
        </section>

        {/* ================= JOB SELECTION ================= */}

        <section className="card">
          <h2>Select Job</h2>

          <p className="section-description">
            Choose a job to view and screen its resumes.
            Changing jobs does not require a new resume upload.
          </p>

          {loadingJobs ? (
            <p>Loading jobs...</p>
          ) : jobs.length === 0 ? (
            <p>No jobs available.</p>
          ) : (
            <div className="job-selector">
              <select
                value={selectedJob?.id ?? ""}
                onChange={(event) => {
                  const jobId = Number(event.target.value);

                  const job = jobs.find(
                    (item) => item.id === jobId,
                  );

                  if (job) {
                    /*
                     * IMPORTANT:
                     *
                     * This only changes selectedJob.
                     * It does NOT upload a resume.
                     */
                    setSelectedJob(job);
                  }
                }}
              >
                {demoJobs.length > 0 && (
                  <optgroup label="Demo Jobs">
                    {demoJobs.map((job) => (
                      <option
                        key={job.id}
                        value={job.id}
                      >
                        {job.title}
                      </option>
                    ))}
                  </optgroup>
                )}

                {myJobs.length > 0 && (
                  <optgroup label="My Jobs">
                    {myJobs.map((job) => (
                      <option
                        key={job.id}
                        value={job.id}
                      >
                        {job.title}
                      </option>
                    ))}
                  </optgroup>
                )}
              </select>
            </div>
          )}
        </section>

        {/* ================= SELECTED JOB ================= */}

        {selectedJob && (
          <>
            <section className="card">
              <div className="job-title-row">
                <h2>{selectedJob.title}</h2>

                {selectedJob.is_demo && (
                  <span className="demo-badge">
                    Demo Job
                  </span>
                )}
              </div>

              <div className="job-details">
                <div>
                  <strong>Description</strong>
                  <p>{selectedJob.description}</p>
                </div>

                <div>
                  <strong>Required Skills</strong>
                  <p>{selectedJob.required_skills}</p>
                </div>

                <div>
                  <strong>Minimum Experience</strong>
                  <p>
                    {selectedJob.min_experience}{" "}
                    {selectedJob.min_experience === 1
                      ? "year"
                      : "years"}
                  </p>
                </div>

                {selectedJob.education && (
                  <div>
                    <strong>Education</strong>
                    <p>{selectedJob.education}</p>
                  </div>
                )}

                {selectedJob.keywords && (
                  <div>
                    <strong>Keywords</strong>
                    <p>{selectedJob.keywords}</p>
                  </div>
                )}
              </div>
            </section>

            {/* ================= OPTIONAL UPLOAD ================= */}

            <section className="card">
              <h2>Upload Resume</h2>

              <p className="section-description">
                Uploading a resume is optional. Resumes uploaded
                for this job will remain associated with this job.
                You can switch to another job without uploading
                anything.
              </p>

              <UploadResume
                jobId={selectedJob.id}
                onUploaded={handleResumeUploaded}
              />
            </section>

            {/* ================= STATISTICS ================= */}

            <section className="stats-grid">
              <div className="stat-card">
                <span className="stat-label">
                  Candidates
                </span>

                <strong className="stat-value">
                  {loadingCandidates
                    ? "..."
                    : candidates.length}
                </strong>
              </div>

              <div className="stat-card">
                <span className="stat-label">
                  Average Score
                </span>

                <strong className="stat-value">
                  {loadingCandidates
                    ? "..."
                    : `${averageScore}%`}
                </strong>
              </div>

              <div className="stat-card">
                <span className="stat-label">
                  Job Type
                </span>

                <strong className="stat-value">
                  {selectedJob.is_demo
                    ? "Demo"
                    : "My Job"}
                </strong>
              </div>
            </section>

            {/* ================= CANDIDATES ================= */}

            <section className="card">
              <div className="section-header">
                <div>
                  <h2>Candidates</h2>

                  <p className="section-description">
                    Candidates already uploaded for{" "}
                    <strong>
                      {selectedJob.title}
                    </strong>
                    .
                  </p>
                </div>
              </div>

              {loadingCandidates ? (
                <div className="loading-state">
                  Loading candidates...
                </div>
              ) : candidates.length === 0 ? (
                <div className="empty-state">
                  <h3>No resumes for this job yet</h3>

                  <p>
                    You do not need to upload a resume just
                    because you selected this job.
                  </p>

                  <p>
                    If you want to test this job, use the
                    optional upload section above.
                  </p>
                </div>
              ) : (
                <div className="candidate-list">
                  {candidates.map((candidate) => (
                    <div
                      key={candidate.resume_id}
                      className="candidate-card"
                    >
                      <div className="candidate-main">
                        <div className="candidate-rank">
                          #{candidate.rank}
                        </div>

                        <div className="candidate-info">
                          <h3>
                            {candidate.candidate_name}
                          </h3>

                          <p>
                            {candidate.candidate_email}
                          </p>

                          <p>
                            {candidate.original_filename}
                          </p>
                        </div>

                        <div className="candidate-score">
                          <strong>
                            {candidate.match_percentage}%
                          </strong>

                          <span>
                            Match
                          </span>
                        </div>
                      </div>

                      <div className="candidate-actions">
                        <button
                          type="button"
                          onClick={() =>
                            setSelectedCandidate(candidate)
                          }
                        >
                          View Details
                        </button>

                        <button
                          type="button"
                          className="delete-button"
                          onClick={() =>
                            handleDeleteResume(
                              candidate.resume_id,
                            )
                          }
                        >
                          Delete Resume
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* ================= CANDIDATE DETAILS ================= */}

            {selectedCandidate && (
              <section className="card">
                <div className="section-header">
                  <div>
                    <h2>Candidate Details</h2>
                    <p className="section-description">
                      Screening result for{" "}
                      <strong>
                        {selectedCandidate.candidate_name}
                      </strong>
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      setSelectedCandidate(null)
                    }
                  >
                    Close
                  </button>
                </div>

                <div className="candidate-details">
                  <div className="detail-row">
                    <strong>Name</strong>
                    <span>
                      {selectedCandidate.candidate_name}
                    </span>
                  </div>

                  <div className="detail-row">
                    <strong>Email</strong>
                    <span>
                      {selectedCandidate.candidate_email}
                    </span>
                  </div>

                  <div className="detail-row">
                    <strong>Resume</strong>
                    <span>
                      {selectedCandidate.original_filename}
                    </span>
                  </div>

                  <div className="detail-row">
                    <strong>Total Score</strong>
                    <span>
                      {selectedCandidate.total_score}%
                    </span>
                  </div>

                  <div className="detail-row">
                    <strong>Recommendation</strong>
                    <span>
                      {selectedCandidate.recommendation}
                    </span>
                  </div>
                </div>

                <div className="score-grid">
                  <div className="score-card">
                    <strong>
                      {selectedCandidate.skill_score}%
                    </strong>
                    <span>Skills</span>
                  </div>

                  <div className="score-card">
                    <strong>
                      {selectedCandidate.experience_score}%
                    </strong>
                    <span>Experience</span>
                  </div>

                  <div className="score-card">
                    <strong>
                      {selectedCandidate.education_score}%
                    </strong>
                    <span>Education</span>
                  </div>

                  <div className="score-card">
                    <strong>
                      {selectedCandidate.keyword_score}%
                    </strong>
                    <span>Keywords</span>
                  </div>
                </div>

                <div className="explanation-section">
                  <h3>Skills Explanation</h3>
                  <p>
                    {selectedCandidate.skills_explanation}
                  </p>

                  <h3>Experience Explanation</h3>
                  <p>
                    {selectedCandidate.experience_explanation}
                  </p>

                  <h3>Education Explanation</h3>
                  <p>
                    {selectedCandidate.education_explanation}
                  </p>

                  <h3>Keywords Explanation</h3>
                  <p>
                    {selectedCandidate.keywords_explanation}
                  </p>
                </div>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;