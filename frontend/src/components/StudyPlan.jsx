
import React from 'react';

export default function StudyPlan({ priorities }) {
    if (!priorities?.length) return <div>No priorities available</div>;

    const studyNow = priorities.filter(p => p.recommendation === 'Study Now');
    const reviseLater = priorities.filter(p => p.recommendation === 'Revise Later');
    const deprioritize = priorities.filter(p => p.recommendation === 'Deprioritize');

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Study Now */}
            <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg shadow-sm">
                <h3 className="text-red-700 font-bold text-lg mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Study Now
                </h3>
                <ul className="space-y-3">
                    {studyNow.map((item, idx) => (
                        <li key={idx} className="bg-white p-3 rounded shadow-sm border border-red-100 flex justify-between items-center group hover:shadow-md transition-shadow">
                            <span className="font-semibold text-gray-800">{item.topic}</span>
                            <span className="text-xs bg-red-100 text-red-600 px-2 py-1 rounded">
                                {(item.priority * 100).toFixed(0)}%
                            </span>
                        </li>
                    ))}
                    {studyNow.length === 0 && <p className="text-gray-500 italic">No urgent tasks!</p>}
                </ul>
            </div>

            {/* Revise Later */}
            <div className="bg-yellow-50 border-l-4 border-yellow-500 p-6 rounded-lg shadow-sm">
                <h3 className="text-yellow-700 font-bold text-lg mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Revise Later
                </h3>
                <ul className="space-y-3">
                    {reviseLater.map((item, idx) => (
                        <li key={idx} className="bg-white p-3 rounded shadow-sm border border-yellow-100 flex justify-between items-center hover:shadow-md transition-shadow">
                            <span className="font-medium text-gray-700">{item.topic}</span>
                            <span className="text-xs text-gray-500">{(item.priority * 100).toFixed(0)}%</span>
                        </li>
                    ))}
                    {reviseLater.length === 0 && <p className="text-gray-500 italic">Nothing to revise.</p>}
                </ul>
            </div>

            {/* Deprioritize */}
            <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg shadow-sm">
                <h3 className="text-green-700 font-bold text-lg mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Deprioritize (Mastered)
                </h3>
                <ul className="space-y-3">
                    {deprioritize.map((item, idx) => (
                        <li key={idx} className="bg-white p-3 rounded shadow-sm border border-green-100 flex justify-between items-center opacity-75 hover:opacity-100 transition-opacity">
                            <span className="text-gray-600 line-through decoration-gray-400">{item.topic}</span>
                            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Done</span>
                        </li>
                    ))}
                    {deprioritize.length === 0 && <p className="text-gray-500 italic">Keep working!</p>}
                </ul>
            </div>
        </div>
    );
}
