import React from "react";
/*
  NOTE:
  - No change needed for Docker
  - Displays recommendations from backend response
*/
export default function CareerRecommendations({ data }) {
  if (!data) return null;

  return (
    <div className="space-y-4 p-4 border rounded">
      <h2 className="text-xl font-bold">Career Recommendations</h2>
      {data.recommendations.map((rec, idx) => (
        <div key={idx} className="p-2 border rounded bg-white">
          <h3 className="font-semibold">{rec.career}</h3>
          <p><strong>Reasoning:</strong> {rec.reasoning}</p>
          <p><strong>Salary:</strong> {rec.avg_salary}</p>
          <p><strong>Growth:</strong> {rec.growth}</p>
          <p><strong>Roadmap:</strong> {rec.roadmap.join(" → ")}</p>
        </div>
      ))}
      {data.alternative_pathways?.length > 0 && (
        <div className="mt-4">
          <h3 className="font-semibold">Alternative Pathways</h3>
          {data.alternative_pathways.map((alt, idx) => (
            <p key={idx}>• {alt.field}: {alt.note}</p>
          ))}
        </div>
      )}
    </div>
  );
}
