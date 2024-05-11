import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);  // Correct initialization
  const [loading, setLoading] = useState(false);  // Loading state

  const startDetection = async () => {
    setLoading(true);  // Set loading to true
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/detection');
      console.log('Response:', response.data);
      setData(response.data);  // Update state
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);  // Reset loading state
    }
  };

  return (
    <div className="App">
      <nav className="bg-[]"></nav>
      <main className="bg-gradient-to-r from-blue-800 to-indigo-900 w-full h-[100vh] flex justify-center items-center">
        <div className="flex justify-center items-center flex-col gap-4 w-1/2">
          <button
            className="bg-[#121481] text-white font-semibold text-2xl p-6 rounded-lg w-1/2"
            onClick={startDetection}
          >
            Start Detection
          </button>
          
        </div>
        <div className="w-1/2">
          {loading ? (  // Show loading message while loading
            <p>Loading...</p>
          ) : data ? (  // Display data if available
            <div className='text-white flex flex-col justify-center items-center '>
            <div className='flex justify-center items-center gap-2'>
              <p className='text-white'>Temperature: {data.temp}</p>
              <p>Turbidity: {data.turbidity}</p>
              <p>Dissolved Oxygen: {data.dissolve_oxygen}</p>
              <p>pH: {data.ph}</p>
            </div>
             
              <p className='text-white'>Predictions: {data.predictions === 0 ? "No Larvae Detected" : "Larvae Detected"}</p>

            </div>
          ) : (  // If data is null, inform user
            <p>No data available.</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
