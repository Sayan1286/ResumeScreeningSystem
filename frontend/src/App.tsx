import {
  useCallback,
  useEffect,
  useState,
} from "react";
import { apiRequest } from "./api";
import Login from "./Login";
import CreateJob from "./CreateJob";
import UploadResume from "./UploadResume";

interface Job {
  id: number;
  recruiter_id: number;
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

function App() {
  const [loggedIn, setLoggedIn] = useState(
    Boolean(localStorage.getItem("access_token")),
  );

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] =
    useState<Job | null>(null);

  const [candidates, setCandidates] =
    useState<ScreeningResult[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedCandidate, setSelectedCandidate] =
    useState<ScreeningResult | null>(null);

  /*
   * Load candidates for the currently selected job.
   * This function can be reused after upload/delete.
   */
  const loadCandidates = useCallback(async () => {
    if (!selectedJob) {
      setCandidates([]);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await apiRequest(
        `/screening/jobs/${selectedJob.id}`,
      );

      setCandidates(data);
    } catch {
      setError("Unable to load screening results.");
    } finally {
      setLoading(false);
    }
  }, [selectedJob]);

  /*
   * Load recruiter jobs.
   */
  useEffect(() => {
    if (!loggedIn) {
      setLoading(false);
      return;
    }

    async function loadJobs() {
      try {
        setLoading(true);
        setError("");

        const data = await apiRequest("/jobs");

        setJobs(data);

        if (data.length > 0) {
          setSelectedJob(data[0]);
        }
      } catch {
        setError("Unable to load jobs.");
      } finally {
        setLoading(false);
      }
    }

    loadJobs();
  }, [loggedIn]);

  /*
   * Automatically load screening results
   * whenever the selected job changes.
   */
  useEffect(() => {
    loadCandidates();
  }, [loadCandidates]);

  /*
   * Delete one resume.
   */
  async function handleDeleteResume(
    resumeId: number,
  ) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this resume?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");

      await apiRequest(`/resumes/${resumeId}`, {
        method: "DELETE",
      });

      setSelectedCandidate(null);

      /*
       * Refresh the candidate list immediately.
       */
      await loadCandidates();
    } catch {
      setError("Unable to delete resume.");
    } finally {
      setLoading(false);
    }
  }

  if (!loggedIn) {
    return (
      <Login
        onLogin={() => setLoggedIn(true)}
      />
    );
  }

  const shortlisted = candidates.filter(
    (candidate) =>
      candidate.status === "Shortlisted",
  );

  const averageScore =
    candidates.length > 0
      ? candidates.reduce(
          (total, candidate) =>
            total + candidate.total_score,
          0,
        ) / candidates.length
      : 0;

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div>
          <h1>Resume Screening System</h1>

          <p>
            AI-powered candidate screening and ranking
          </p>
        </div>

        <button
          onClick={() => {
            localStorage.removeItem(
              "access_token",
            );

            setLoggedIn(false);
            setCandidates([]);
            setSelectedCandidate(null);
          }}
        >
          Logout
        </button>
      </header>

      <main className="dashboard">

        {/* Welcome */}
        <section className="welcome-card">
          <h2>Recruiter Dashboard</h2>

          <p>
            Create jobs, upload resumes, and screen
            candidates based on skills, experience,
            education, and keywords.
          </p>
        </section>

        {/* Create Job */}
        <CreateJob
          onJobCreated={() => {
            window.location.reload();
          }}
        />

        {/* Upload Resume */}
        {selectedJob && (
          <UploadResume
            jobId={selectedJob.id}
            onUploaded={async () => {
              setSelectedCandidate(null);

              /*
               * Automatically refresh candidates
               * after successful upload.
               */
              await loadCandidates();
            }}
          />
        )}

        {/* Loading */}
        {loading && (
          <p>Loading screening results...</p>
        )}

        {/* Error */}
        {error && (
          <p className="error">{error}</p>
        )}

        {!loading && !error && (
          <>

            {/* Statistics */}
            <section className="stats">

              <div className="stat-card">
                <h3>Candidates</h3>

                <strong>
                  {candidates.length}
                </strong>
              </div>

              <div className="stat-card">
                <h3>Screened Resumes</h3>

                <strong>
                  {candidates.length}
                </strong>
              </div>

              <div className="stat-card">
                <h3>Shortlisted</h3>

                <strong>
                  {shortlisted.length}
                </strong>
              </div>

              <div className="stat-card">
                <h3>Average Score</h3>

                <strong>
                  {averageScore.toFixed(2)}%
                </strong>
              </div>

            </section>

            {/* Job Section */}
            <section className="job-card">

              {/* Job Selector */}
              {jobs.length > 1 && (
                <section className="welcome-card">
                  <h2>Select Job</h2>

                  <select
                    value={
                      selectedJob?.id ?? ""
                    }
                    onChange={(event) => {
                      const job = jobs.find(
                        (item) =>
                          item.id ===
                          Number(
                            event.target.value,
                          ),
                      );

                      setSelectedJob(
                        job ?? null,
                      );

                      setSelectedCandidate(
                        null,
                      );
                    }}
                  >
                    {jobs.map((job) => (
                      <option
                        key={job.id}
                        value={job.id}
                      >
                        {job.title}
                      </option>
                    ))}
                  </select>
                </section>
              )}

              {/* Selected Job */}
              <div>
                <h2>
                  {selectedJob?.title}
                </h2>

                <p>
                  {selectedJob?.required_skills}{" "}
                  •{" "}
                  {selectedJob?.education ??
                    "Any education"}{" "}
                  •{" "}
                  {selectedJob?.min_experience}
                  + years experience
                </p>
              </div>

              <button
                onClick={() =>
                  setSelectedCandidate(
                    candidates[0] ?? null,
                  )
                }
                disabled={
                  candidates.length === 0
                }
              >
                View Candidates
              </button>

            </section>

            {/* Candidate Ranking */}
            <section className="welcome-card">

              <h2>Candidate Ranking</h2>

              {candidates.length === 0 && (
                <p>
                  No candidates have been
                  screened for this job yet.
                </p>
              )}

              <div className="candidate-list">

                {candidates.map(
                  (candidate) => (
                    <div
                      className="candidate-card"
                      key={candidate.resume_id}
                    >

                      {/* Candidate Header */}
                      <div className="candidate-header">

                        <div>
                          <h3>
                            #{candidate.rank}{" "}
                            {
                              candidate.candidate_name
                            }
                          </h3>

                          <p>
                            {
                              candidate.candidate_email
                            }
                          </p>
                        </div>

                        <div className="candidate-score">

                          <strong>
                            {candidate.match_percentage.toFixed(
                              2,
                            )}
                            %
                          </strong>

                          <span>
                            {candidate.status}
                          </span>

                        </div>

                      </div>

                      {/* Candidate Summary */}
                      <div className="candidate-summary">

                        <p>
                          <strong>
                            Skills:
                          </strong>{" "}
                          {
                            candidate.skills_explanation
                          }
                        </p>

                        <p>
                          <strong>
                            Experience:
                          </strong>{" "}
                          {
                            candidate.experience_explanation
                          }
                        </p>

                        <p>
                          <strong>
                            Education:
                          </strong>{" "}
                          {
                            candidate.education_explanation
                          }
                        </p>

                        <p>
                          <strong>
                            Keywords:
                          </strong>{" "}
                          {
                            candidate.keywords_explanation
                          }
                        </p>

                      </div>

                      {/* Candidate Actions */}
                      <div className="candidate-actions">

                        <button
                          onClick={() =>
                            setSelectedCandidate(
                              candidate,
                            )
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
                  ),
                )}

              </div>

            </section>

            {/* Candidate Details */}
            {selectedCandidate && (
              <section className="welcome-card candidate-details">

                {/* Details Header */}
                <div className="details-header">

                  <div>
                    <h2>
                      Candidate Details
                    </h2>

                    <p>
                      Detailed screening
                      information for{" "}
                      {
                        selectedCandidate.candidate_name
                      }
                    </p>
                  </div>

                  <div className="candidate-actions">

                    <button
                      onClick={() =>
                        setSelectedCandidate(
                          null,
                        )
                      }
                    >
                      Close
                    </button>

                    <button
                      type="button"
                      className="delete-button"
                      onClick={() =>
                        handleDeleteResume(
                          selectedCandidate.resume_id,
                        )
                      }
                    >
                      Delete Resume
                    </button>

                  </div>

                </div>

                {/* Candidate Information */}
                <div className="details-candidate">

                  <h3>
                    {
                      selectedCandidate.candidate_name
                    }
                  </h3>

                  <p>
                    <strong>
                      Email:
                    </strong>{" "}
                    {
                      selectedCandidate.candidate_email
                    }
                  </p>

                  <p>
                    <strong>
                      Resume:
                    </strong>{" "}
                    {
                      selectedCandidate.original_filename
                    }
                  </p>

                </div>

                {/* Overall Score */}
                <div className="details-score">

                  <h3>
                    Overall Match
                  </h3>

                  <strong>
                    {selectedCandidate.match_percentage.toFixed(
                      2,
                    )}
                    %
                  </strong>

                  <p>
                    {
                      selectedCandidate.recommendation
                    }
                  </p>

                </div>

                {/* Score Breakdown */}
                <h3>
                  Score Breakdown
                </h3>

                <div className="score-breakdown">

                  <div>
                    <span>
                      Skills
                    </span>

                    <strong>
                      {
                        selectedCandidate.skill_score
                      }
                    </strong>
                  </div>

                  <div>
                    <span>
                      Experience
                    </span>

                    <strong>
                      {
                        selectedCandidate.experience_score
                      }
                    </strong>
                  </div>

                  <div>
                    <span>
                      Education
                    </span>

                    <strong>
                      {
                        selectedCandidate.education_score
                      }
                    </strong>
                  </div>

                  <div>
                    <span>
                      Keywords
                    </span>

                    <strong>
                      {
                        selectedCandidate.keyword_score
                      }
                    </strong>
                  </div>

                </div>

                {/* Screening Explanation */}
                <h3>
                  Screening Explanation
                </h3>

                <div className="explanation-list">

                  <p>
                    <strong>
                      Skills:
                    </strong>{" "}
                    {
                      selectedCandidate.skills_explanation
                    }
                  </p>

                  <p>
                    <strong>
                      Experience:
                    </strong>{" "}
                    {
                      selectedCandidate.experience_explanation
                    }
                  </p>

                  <p>
                    <strong>
                      Education:
                    </strong>{" "}
                    {
                      selectedCandidate.education_explanation
                    }
                  </p>

                  <p>
                    <strong>
                      Keywords:
                    </strong>{" "}
                    {
                      selectedCandidate.keywords_explanation
                    }
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