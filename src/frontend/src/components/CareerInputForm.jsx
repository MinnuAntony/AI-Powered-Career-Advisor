import React, { useState } from "react";

/* Component to input grades & interests */
export default function CareerInputForm({ onSubmit }) {
  const [subjects, setSubjects] = useState([{ name: "Math", score: "" }]);
  const [interests, setInterests] = useState("");

  // Add a new subject row
  const addSubject = () => {
    setSubjects([...subjects, { name: "", score: "" }]);
  };

  // Update subject/score values
  const handleChange = (index, field, value) => {
    const updated = [...subjects];
    updated[index][field] = value;
    setSubjects(updated);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Convert subjects array -> grades object
    const grades = {};
    subjects.forEach((sub) => {
      if (sub.name && sub.score) {
        grades[sub.name.toLowerCase()] = Number(sub.score);
      }
    });

    onSubmit({ grades, interests });
  };

  return (
    <form
      className="space-y-6 p-6 bg-white shadow-lg rounded-xl border border-gray-200"
      onSubmit={handleSubmit}
    >
      <h2 className="text-2xl font-bold text-gray-800 mb-2">
        Student Information
      </h2>
      <p className="text-sm text-gray-500 mb-4">
        Enter your subjects, scores (out of 100), and interests to continue.
      </p>

      {/* Dynamic subjects */}
      {subjects.map((sub, idx) => (
        <div key={idx} className="flex gap-3 items-center">
          <input
            type="text"
            placeholder="Subject"
            value={sub.name}
            onChange={(e) => handleChange(idx, "name", e.target.value)}
            className="border border-gray-300 p-2 rounded-lg w-1/2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          <input
            type="number"
            placeholder="Score"
            value={sub.score}
            onChange={(e) => handleChange(idx, "score", e.target.value)}
            className="border border-gray-300 p-2 rounded-lg w-1/2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            min={0}
            max={100}
          />
        </div>
      ))}

      <button
        type="button"
        onClick={addSubject}
        className="px-3 py-1 bg-gray-100 border border-gray-300 text-sm rounded-lg hover:bg-gray-200 transition"
      >
        + Add Subject
      </button>

      {/* Interests */}
      <div>
        <label className="block font-medium text-gray-700 mb-1">Interests</label>
        <textarea
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          className="border border-gray-300 p-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500 focus:outline-none"
          rows="3"
          placeholder="E.g., I enjoy coding, robotics, problem-solving"
        />
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition w-full font-medium shadow-sm"
      >
        Next →
      </button>
    </form>
  );
}
