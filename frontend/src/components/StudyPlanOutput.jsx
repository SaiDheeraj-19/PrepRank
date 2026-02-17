import PropTypes from 'prop-types';
import './StudyPlanOutput.css';

function StudyPlanOutput({ studyPlan }) {
    if (!studyPlan || !studyPlan.priorities || studyPlan.priorities.length === 0) {
        return null;
    }

    const { student_id, generated_at, priorities } = studyPlan;

    // Group by category
    const studyNow = priorities.filter(p => p.recommendation === 'Study Now');
    const reviseLater = priorities.filter(p => p.recommendation === 'Revise Later');
    const mastered = priorities.filter(p => p.recommendation === 'Mastered');
    const deprioritize = priorities.filter(p => p.recommendation === 'Deprioritize');

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const handleCopy = () => {
        const text = document.getElementById('study-plan-text').innerText;
        navigator.clipboard.writeText(text);
        alert('Study plan copied to clipboard!');
    };

    const handleDownload = () => {
        const text = document.getElementById('study-plan-text').innerText;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `study-plan-student-${student_id}.txt`;
        a.click();
        window.URL.revokeObjectURL(url);
    };

    return (
        <div className="study-plan-output">
            <div className="output-header">
                <div className="output-actions">
                    <button onClick={handleCopy} className="action-btn">
                        📋 Copy to Clipboard
                    </button>
                    <button onClick={handleDownload} className="action-btn">
                        💾 Download as Text
                    </button>
                </div>
            </div>

            <div className="output-content" id="study-plan-text">
                <div className="output-section">
                    <h2>📚 PERSONALIZED STUDY PLAN</h2>
                    <p><strong>Student ID:</strong> {student_id}</p>
                    <p><strong>Generated:</strong> {formatDate(generated_at)}</p>
                    <p><strong>Total Topics Analyzed:</strong> {priorities.length}</p>
                </div>

                <div className="output-divider">═══════════════════════════════════════</div>

                {studyNow.length > 0 && (
                    <div className="output-section">
                        <h3>🔴 IMMEDIATE PRIORITY - Study These Now ({studyNow.length} topics)</h3>
                        <p className="section-description">
                            These topics have HIGH exam importance but LOW your mastery.
                            Focus here to maximize score improvement.
                        </p>
                        <ol>
                            {studyNow.map((topic, idx) => (
                                <li key={idx}>
                                    <strong>{topic.topic_name}</strong> ({topic.subject})
                                    <div className="topic-details">
                                        - Priority: {(topic.priority_score * 100).toFixed(0)}% |
                                        Exam Importance: {(topic.importance_score * 100).toFixed(0)}% |
                                        Your Mastery: {(topic.mastery_score * 100).toFixed(0)}%
                                    </div>
                                    <div className="topic-reason">
                                        → Why: Critical exam topic where you're currently weak
                                    </div>
                                </li>
                            ))}
                        </ol>
                    </div>
                )}

                {reviseLater.length > 0 && (
                    <>
                        <div className="output-divider">───────────────────────────────────────</div>
                        <div className="output-section">
                            <h3>🟡 SECONDARY PRIORITY - Revise After Core Topics ({reviseLater.length} topics)</h3>
                            <p className="section-description">
                                Moderate priority topics. Schedule these after completing "Study Now" items.
                            </p>
                            <ul>
                                {reviseLater.map((topic, idx) => (
                                    <li key={idx}>
                                        <strong>{topic.topic_name}</strong> ({topic.subject}) -
                                        Priority: {(topic.priority_score * 100).toFixed(0)}%
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </>
                )}

                {mastered.length > 0 && (
                    <>
                        <div className="output-divider">───────────────────────────────────────</div>
                        <div className="output-section">
                            <h3>⭐ EXCELLENT WORK - Already Mastered ({mastered.length} topics)</h3>
                            <p className="section-description">
                                You've demonstrated strong performance here. Light periodic review is sufficient.
                            </p>
                            <ul>
                                {mastered.map((topic, idx) => (
                                    <li key={idx}>
                                        <strong>{topic.topic_name}</strong> ({topic.subject}) -
                                        Mastery: {(topic.mastery_score * 100).toFixed(0)}%
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </>
                )}

                {deprioritize.length > 0 && (
                    <>
                        <div className="output-divider">───────────────────────────────────────</div>
                        <div className="output-section">
                            <h3>🟢 LOW PRIORITY - Deprioritize ({deprioritize.length} topics)</h3>
                            <p className="section-description">
                                Lower exam weightage or already decent mastery. Study only if time permits.
                            </p>
                            <ul>
                                {deprioritize.map((topic, idx) => (
                                    <li key={idx}>
                                        {topic.topic_name} ({topic.subject})
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </>
                )}

                <div className="output-divider">═══════════════════════════════════════</div>

                <div className="output-section">
                    <h3>📊 RECOMMENDED ACTION PLAN</h3>
                    <ol className="action-plan">
                        <li><strong>This Week:</strong> Complete all "Study Now" topics with practice problems</li>
                        <li><strong>Next Week:</strong> Begin "Revise Later" topics and re-test "Study Now" areas</li>
                        <li><strong>Ongoing:</strong> Light review of "Mastered" topics every 2 weeks (spaced repetition)</li>
                        <li><strong>Mock Tests:</strong> Take practice tests monthly to update this plan automatically</li>
                    </ol>
                </div>

                <div className="output-footer">
                    <p><em>This plan is data-driven and updates based on your performance.</em></p>
                    <p><em>Formula: Priority = Exam Importance × (1 - Your Mastery)</em></p>
                    <p>─────────────────────────────────────</p>
                    <p><small>Generated by Study Priority Engine v1.0</small></p>
                </div>
            </div>
        </div>
    );
}

StudyPlanOutput.propTypes = {
    studyPlan: PropTypes.shape({
        student_id: PropTypes.number.isRequired,
        generated_at: PropTypes.string.isRequired,
        priorities: PropTypes.arrayOf(
            PropTypes.shape({
                topic_name: PropTypes.string.isRequired,
                subject: PropTypes.string.isRequired,
                importance_score: PropTypes.number.isRequired,
                mastery_score: PropTypes.number.isRequired,
                priority_score: PropTypes.number.isRequired,
                recommendation: PropTypes.string.isRequired
            })
        ).isRequired
    }).isRequired
};

export default StudyPlanOutput;
