// import React, { useState } from "react";
// import CareerInputForm from "../components/CareerInputForm";
// import AssessmentForm from "../components/AssessmentForm";
// import CareerRecommendations from "../components/CareerRecommendations";
// import { submitCareerRequest, submitAssessment } from "../api/api";

// export default function Home() {
//   const [careerData, setCareerData] = useState(null);
//   const [formData, setFormData] = useState(null);
//   const [assessmentData, setAssessmentData] = useState(null);
//   const [showAssessment, setShowAssessment] = useState(false);

//   const handleCareerSubmit = async (data) => {
//     setFormData(data);
//     setShowAssessment(true);
//   };

//   const handleAssessmentSubmit = async (answers) => {
//     const assessment = await submitAssessment(answers);
//     setAssessmentData(assessment);

//     // Combine grades/interests + assessment for final career request
//     const finalData = { ...formData, assessment };
//     const result = await submitCareerRequest(finalData);
//     setCareerData(result);
//   };

//   return (
//     <div className="max-w-4xl mx-auto p-4 space-y-6">
//       {!showAssessment && <CareerInputForm onSubmit={handleCareerSubmit} />}
//       {showAssessment && !careerData && <AssessmentForm onSubmit={handleAssessmentSubmit} />}
//       {careerData && <CareerRecommendations data={careerData} />}
//     </div>
//   );
// }
import React, { useState } from "react";
import CareerInputForm from "../components/CareerInputForm";
import AssessmentForm from "../components/AssessmentForm";
import CareerRecommendations from "../components/CareerRecommendations";
import { submitCareerRequest } from "../api/api"; // only need this now

export default function Home() {
  const [careerData, setCareerData] = useState(null);
  const [formData, setFormData] = useState(null);
  const [showAssessment, setShowAssessment] = useState(false);

  const handleCareerSubmit = async (data) => {
    setFormData(data);
    setShowAssessment(true);
  };

  const handleAssessmentSubmit = async (assessment) => {
    try {
      // Combine grades/interests + assessment for final career request
      const finalData = { ...formData, assessment };
      
      // Send directly to /recommend
      const result = await submitCareerRequest(finalData);
      setCareerData(result);
    } catch (err) {
      console.error(err.response?.data || err);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      {!showAssessment && <CareerInputForm onSubmit={handleCareerSubmit} />}
      {showAssessment && !careerData && <AssessmentForm onSubmit={handleAssessmentSubmit} />}
      {careerData && <CareerRecommendations data={careerData} />}
    </div>
  );
}
