
import React from 'react';

export default function TopicPriorityTable({ priorities }) {
    if (!priorities?.length) return <div>No data available</div>;

    return (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Topic Priority List</h2>
            <div className="overflow-x-auto">
                <table className="w-full text-left">
                    <thead className="bg-gray-50 text-gray-600 text-sm">
                        <tr>
                            <th className="px-4 py-3">Topic</th>
                            <th className="px-4 py-3">Importance</th>
                            <th className="px-4 py-3">Mastery</th>
                            <th className="px-4 py-3">Priority Score</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {priorities.map((item, index) => (
                            <tr key={index} className="hover:bg-gray-50 transition-colors">
                                <td className="px-4 py-3 font-medium text-gray-800">{item.topic}</td>
                                <td className="px-4 py-3">
                                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                                        {item.importance.toFixed(2)}
                                    </span>
                                </td>
                                <td className="px-4 py-3">
                                    <span className={`text-xs px-2 py-1 rounded-full ${item.mastery > 0.7 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                        }`}>
                                        {item.mastery.toFixed(2)}
                                    </span>
                                </td>
                                <td className="px-4 py-3 font-semibold text-gray-900">
                                    {(item.priority * 100).toFixed(1)}%
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
