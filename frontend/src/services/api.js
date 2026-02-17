
const API_BASE_URL = 'http://localhost:8000';

export const getTopicPriorities = async () => {
    try {
        // Fetch format: { student_id, generated_at, priorities: [...] }
        const response = await fetch(`${API_BASE_URL}/study-plan/1`); 
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        
        // Transform for frontend if needed (currently matches well)
        return data.priorities.map(item => ({
            topic: item.topic_name,
            importance: item.importance_score,
            mastery: item.mastery_score,
            priority: item.priority_score,
            recommendation: item.recommendation
        }));
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
};

export const getStudyPlan = async () => {
    try {
        const priorities = await getTopicPriorities();
        
        return {
            study_now: priorities.filter(p => p.recommendation === 'Study Now').map(p => p.topic),
            revise_later: priorities.filter(p => p.recommendation === 'Revise Later').map(p => p.topic),
            deprioritize: priorities.filter(p => p.recommendation === 'Deprioritize').map(p => p.topic)
        };
    } catch (error) {
        return { study_now: [], revise_later: [], deprioritize: [] };
    }
};
