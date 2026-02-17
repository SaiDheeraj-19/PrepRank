
import React, { useEffect, useState } from 'react';
import { getTopicPriorities } from './services/api';
import TopicPriorityTable from './components/TopicPriorityTable';
import StudyPlan from './components/StudyPlan';
import PriorityChart from './components/PriorityChart';

function App() {
  const [priorities, setPriorities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getTopicPriorities();
        setPriorities(data.sort((a, b) => b.priority - a.priority)); // Sort high to low
        setLoading(false);
      } catch (err) {
        setError("Failed to load data. Is the backend running?");
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 text-gray-500">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
      Loading Study Engine...
    </div>
  );

  if (error) return (
    <div className="min-h-screen flex items-center justify-center bg-red-50 text-red-600">
      <span className="font-bold">Error:</span> {error}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <span className="bg-blue-600 text-white rounded-lg p-2 font-bold shadow-md">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </span>
            <h1 className="text-2xl font-extrabold text-gray-900 tracking-tight">
              Study Priority <span className="text-blue-600">Engine</span>
            </h1>
          </div>
          <button className="text-sm text-gray-500 hover:text-gray-900 font-medium transition-colors">
            Demo Student #1
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        {/* Section 1: Study Plan (Top Priority) */}
        <section>
          <h2 className="text-xl font-semibold mb-4 text-gray-700 uppercase tracking-wider text-xs border-b pb-2">Your Action Plan</h2>
          <StudyPlan priorities={priorities} />
        </section>

        {/* Section 2: Visualization */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-700 uppercase tracking-wider text-xs border-b pb-2">Analysis</h2>
            <PriorityChart priorities={priorities} />
          </div>
          <div>
            <h2 className="text-xl font-semibold mb-4 text-gray-700 uppercase tracking-wider text-xs border-b pb-2">Detailed Metrics</h2>
            <TopicPriorityTable priorities={priorities} />
          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12 py-8 text-center text-gray-400 text-sm">
        <p>© 2026 Study Priority Engine. Built for student success.</p>
      </footer>

    </div>
  );
}

export default App;
