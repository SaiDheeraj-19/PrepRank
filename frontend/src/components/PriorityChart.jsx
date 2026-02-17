
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function PriorityChart({ priorities }) {
    if (!priorities?.length) return <div>No chart data</div>;

    const data = priorities.map(item => ({
        name: item.topic,
        Priority: (item.priority * 100).toFixed(1),
        Mastery: (item.mastery * 100).toFixed(1),
    }));

    return (
        <div className="bg-white p-6 rounded-lg shadow-xl border border-gray-200" style={{ height: 400 }}>
            <h3 className="text-lg font-bold mb-4 text-center text-gray-700">Topic Priority vs Mastery</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={data}
                    margin={{
                        top: 20,
                        right: 30,
                        left: 20,
                        bottom: 60, // Extra space for labels
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ccc" />
                    <XAxis
                        dataKey="name"
                        angle={-45}
                        textAnchor="end"
                        height={80}
                        tick={{ fontSize: 12, fill: '#666' }}
                        stroke="#888"
                    />
                    <YAxis stroke="#888" />
                    <Tooltip
                        cursor={{ fill: 'rgba(0,0,0,0.05)' }}
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
                    />
                    <Legend wrapperStyle={{ paddingTop: '20px' }} />
                    <Bar dataKey="Priority" fill="#ef4444" radius={[4, 4, 0, 0]} barSize={20} name="Priority Score (%)" />
                    <Bar dataKey="Mastery" fill="#22c55e" radius={[4, 4, 0, 0]} barSize={20} name="Current Mastery (%)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
