// import React, { useState } from "react";

// export default function ChatBotPage() {
//   const [question, setQuestion] = useState("");
//   const [answer, setAnswer] = useState("");
//   const [loading, setLoading] = useState(false);

//   async function askQuestion() {
//     if (!question.trim()) return;
//     setLoading(true);
//     setAnswer("");
//     const q = question;
//     setQuestion("");

//     try {
//       const res = await fetch("http://localhost:8000/api/v1/ask", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ question: q }),
//       });
//       const data = await res.json();

//       // typewriter effect
//       let i = 0;
//       const text = data.answer || "No answer received.";
//       setAnswer("");
//       const interval = setInterval(() => {
//         setAnswer((prev) => prev + text[i]);
//         i++;
//         if (i >= text.length) clearInterval(interval);
//       }, 20);
//     } catch (err) {
//       console.error(err);
//       setAnswer("Error: Could not reach the server.");
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
//       <div className="max-w-lg w-full bg-white shadow-md rounded-lg p-6">
//         <h2 className="text-2xl font-bold mb-4">AI Q&A Chat</h2>
//         <div className="flex space-x-2">
//           <input
//             type="text"
//             value={question}
//             onChange={(e) => setQuestion(e.target.value)}
//             onKeyDown={(e) => e.key === "Enter" && askQuestion()}
//             placeholder="Ask me anything..."
//             className="flex-1 border rounded px-3 py-2"
//           />
//           <button
//             onClick={askQuestion}
//             className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//           >
//             Ask
//           </button>
//         </div>

//         <div className="mt-4 p-3 bg-gray-100 rounded min-h-[50px] whitespace-pre-wrap">
//           {loading ? (
//             <div className="flex space-x-1">
//               <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></span>
//               <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.2s]"></span>
//               <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.4s]"></span>
//             </div>
//           ) : (
//             answer
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }
import React, { useState } from "react";

export default function ChatBotPage() {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]); // store all Q/A pairs
  const [loading, setLoading] = useState(false);

  async function askQuestion() {
    if (!question.trim()) return;
    setLoading(true);
    const q = question;
    setQuestion("");

    try {
      const res = await fetch("http://localhost:8000/api/v1/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();

      // typewriter effect for this answer
      let i = 0;
      const text = data.answer || "No answer received.";
      let answerText = "";

      const interval = setInterval(() => {
        answerText += text[i];
        i++;
        setChat((prev) => {
          // replace last entry while typing
          const updated = [...prev];
          if (updated[updated.length - 1]?.typing) {
            updated[updated.length - 1].answer = answerText;
          } else {
            updated.push({ question: q, answer: answerText, typing: true });
          }
          return updated;
        });
        if (i >= text.length) {
          clearInterval(interval);
          setChat((prev) =>
            prev.map((item, idx) =>
              idx === prev.length - 1 ? { ...item, typing: false } : item
            )
          );
        }
      }, 20);
    } catch (err) {
      console.error(err);
      setChat((prev) => [...prev, { question: q, answer: "Error: Could not reach server", typing: false }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="max-w-lg w-full bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4">AI Q&A Chat</h2>

        <div className="flex space-x-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askQuestion()}
            placeholder="Ask me anything..."
            className="flex-1 border rounded px-3 py-2"
          />
          <button
            onClick={askQuestion}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Ask
          </button>
        </div>

        <div className="mt-4 p-3 bg-gray-100 rounded max-h-[400px] overflow-y-auto whitespace-pre-wrap">
          {chat.map((turn, idx) => (
            <div key={idx} className="mb-3">
              <p><b>Q:</b> {turn.question}</p>
              <p><b>A:</b> {turn.answer}</p>
            </div>
          ))}

          {loading && (
            <div className="flex space-x-1">
              <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.2s]"></span>
              <span className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.4s]"></span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
