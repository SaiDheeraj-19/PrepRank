import PropTypes from 'prop-types';
import './PriorityList.css';

const CATEGORY_CONFIG = {
    'Study Now': {
        color: '#ef4444',
        gradient: 'linear-gradient(135deg, #f87171, #dc2626)',
        icon: '🔴',
        description: 'High importance, low mastery - Start immediately'
    },
    'Revise Later': {
        color: '#f59e0b',
        gradient: 'linear-gradient(135deg, #fbbf24, #f59e0b)',
        icon: '🟡',
        description: 'Moderate priority - Schedule for review'
    },
    'Mastered': {
        color: '#10b981',
        gradient: 'linear-gradient(135deg, #34d399, #059669)',
        icon: '⭐',
        description: 'Excellent performance - Maintain with light review'
    },
    'Deprioritize': {
        color: '#6b7280',
        gradient: 'linear-gradient(135deg, #9ca3af, #6b7280)',
        icon: '🟢',
        description: 'Low yield - Focus on higher priorities first'
    }
};

function PriorityCard({ topic, rank }) {
    const config = CATEGORY_CONFIG[topic.recommendation] || CATEGORY_CONFIG['Deprioritize'];

    return (
        <div className="priority-card" style={{ borderLeftColor: config.color }}>
            <div className="card-header">
                <div className="rank-badge" style={{ background: config.gradient }}>
                    #{rank}
                </div>
                <div className="category-badge" style={{ background: config.gradient }}>
                    {config.icon} {topic.recommendation}
                </div>
            </div>

            <div className="card-body">
                <h3 className="topic-name">{topic.topic_name}</h3>
                <p className="subject-name">{topic.subject}</p>

                <div className="metrics-grid">
                    <div className="metric">
                        <span className="metric-label">Priority Score</span>
                        <div className="metric-value-container">
                            <div
                                className="metric-bar"
                                style={{
                                    width: `${topic.priority_score * 100}%`,
                                    background: config.gradient
                                }}
                            ></div>
                            <span className="metric-value">
                                {(topic.priority_score * 100).toFixed(0)}%
                            </span>
                        </div>
                    </div>

                    <div className="metric">
                        <span className="metric-label">Exam Importance</span>
                        <div className="metric-value-container">
                            <div
                                className="metric-bar importance"
                                style={{ width: `${topic.importance_score * 100}%` }}
                            ></div>
                            <span className="metric-value">
                                {(topic.importance_score * 100).toFixed(0)}%
                            </span>
                        </div>
                    </div>

                    <div className="metric">
                        <span className="metric-label">Your Mastery</span>
                        <div className="metric-value-container">
                            <div
                                className="metric-bar mastery"
                                style={{ width: `${topic.mastery_score * 100}%` }}
                            ></div>
                            <span className="metric-value">
                                {(topic.mastery_score * 100).toFixed(0)}%
                            </span>
                        </div>
                    </div>
                </div>

                <div className="recommendation-text">
                    <small>{config.description}</small>
                </div>
            </div>
        </div>
    );
}

PriorityCard.propTypes = {
    topic: PropTypes.shape({
        topic_name: PropTypes.string.isRequired,
        subject: PropTypes.string.isRequired,
        importance_score: PropTypes.number.isRequired,
        mastery_score: PropTypes.number.isRequired,
        priority_score: PropTypes.number.isRequired,
        recommendation: PropTypes.string.isRequired
    }).isRequired,
    rank: PropTypes.number.isRequired
};

function PriorityList({ priorities }) {
    if (!priorities || priorities.length === 0) {
        return (
            <div className="empty-priorities">
                <p>No priorities to display</p>
            </div>
        );
    }

    // Group by category
    const grouped = priorities.reduce((acc, topic) => {
        const category = topic.recommendation;
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push(topic);
        return acc;
    }, {});

    const categoryOrder = ['Study Now', 'Revise Later', 'Mastered', 'Deprioritize'];

    return (
        <div className="priority-list">
            {categoryOrder.map(category => {
                const topics = grouped[category];
                if (!topics || topics.length === 0) return null;

                return (
                    <div key={category} className="category-section">
                        <h3 className="category-header">
                            {CATEGORY_CONFIG[category].icon} {category} ({topics.length})
                        </h3>
                        <div className="cards-grid">
                            {topics.map((topic, index) => (
                                <PriorityCard
                                    key={`${topic.topic_name}-${index}`}
                                    topic={topic}
                                    rank={priorities.indexOf(topic) + 1}
                                />
                            ))}
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

PriorityList.propTypes = {
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
};

export default PriorityList;
