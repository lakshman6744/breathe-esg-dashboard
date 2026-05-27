import { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [dashboard, setDashboard] = useState(null);
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const fetchDashboard = () => {

    axios.get("http://127.0.0.1:8000/api/dashboard/")
      .then((response) => {
        setDashboard(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData
      );

      setMessage(response.data.message);

      fetchDashboard();

    } catch (error) {

      console.log(error);

      setMessage("Upload failed");
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>ESG Emissions Dashboard</h1>

      <br />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        style={{
          marginLeft: "10px",
          padding: "8px 15px"
        }}
      >
        Upload CSV
      </button>

      <p>{message}</p>

      <hr />

      {dashboard ? (
        <div>

          <h2>Total Records: {dashboard.total_records}</h2>

          <h2>Total Emissions: {dashboard.total_emissions}</h2>

          <h2>Suspicious Records: {dashboard.suspicious_records}</h2>

        </div>
      ) : (
        <h2>Loading...</h2>
      )}

    </div>
  );
}

export default App;