
// import React, { useState } from "react";

// /* Component to input grades & interests */
// export default function CareerInputForm({ onSubmit }) {
//   const [grades, setGrades] = useState({ math: "", english: "" });
//   const [interests, setInterests] = useState("");

//   const handleGradeChange = (subject, value) => {
//     setGrades({ ...grades, [subject]: value });
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     const numericGrades = Object.fromEntries(
//       Object.entries(grades).map(([k, v]) => [k, Number(v)])
//     );
//     onSubmit({ grades: numericGrades, interests });
//   };

//   return (
//     <form className="space-y-4 p-4 border rounded" onSubmit={handleSubmit}>
//       <h2 className="text-xl font-bold">Student Info</h2>
//       {Object.keys(grades).map((subject) => (
//         <div key={subject}>
//           <label className="block">{subject}</label>
//           <input
//             type="number"
//             value={grades[subject]}
//             onChange={(e) => handleGradeChange(subject, e.target.value)}
//             className="border p-1 rounded w-full"
//             min={0}
//             max={100}
//           />
//         </div>
//       ))}
//       <div>
//         <label className="block">Interests</label>
//         <input
//           type="text"
//           value={interests}
//           onChange={(e) => setInterests(e.target.value)}
//           className="border p-1 rounded w-full"
//           placeholder="E.g., I enjoy coding and robotics"
//         />
//       </div>
//       <button className="bg-blue-500 text-white px-4 py-2 rounded">Next</button>
//     </form>
//   );
// }


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
      className="space-y-6 p-6 bg-white shadow-md rounded-lg"
      onSubmit={handleSubmit}
    >
      <h2 className="text-2xl font-bold text-gray-800">Student Information</h2>

      {/* Dynamic subjects */}
      {subjects.map((sub, idx) => (
        <div key={idx} className="flex gap-3 items-center">
          <input
            type="text"
            placeholder="Subject"
            value={sub.name}
            onChange={(e) => handleChange(idx, "name", e.target.value)}
            className="border p-2 rounded w-1/2"
          />
          <input
            type="number"
            placeholder="Score"
            value={sub.score}
            onChange={(e) => handleChange(idx, "score", e.target.value)}
            className="border p-2 rounded w-1/2"
            min={0}
            max={100}
          />
        </div>
      ))}

      <button
        type="button"
        onClick={addSubject}
        className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
      >
        + Add Subject
      </button>

      {/* Interests */}
      <div>
        <label className="block font-medium text-gray-700">Interests</label>
        <textarea
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          className="border p-2 rounded w-full"
          rows="3"
          placeholder="E.g., I enjoy coding, robotics, problem-solving"
        />
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
      >
        Next
      </button>
    </form>
  );
}
