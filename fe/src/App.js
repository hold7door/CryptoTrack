import logo from "./logo.svg";
import "./App.css";
import { Chart } from "frappe-charts/dist/frappe-charts.min.esm";

import { format, subDays, subSeconds } from "date-fns";
import axios from "axios";

import styled from "styled-components";
import { useEffect, useState } from "react";

function App() {
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    if (!graphData) {
      const apiRequest = async () => {
        try {
          const response = await axios.post("http://127.0.0.1:8000/daily", {
            time_range: "7d",
          });
          setGraphData(response.data.result);
        } catch (err) {
          console.log(err);
        }
      };
      apiRequest();
    }

    if (!graphData) return;

    const dates = [];

    let today = new Date(new Date().toUTCString());
    for (let i = 0; i < 7; i++) {
      let prevDay = subDays(today, 1);
      let todayString = format(today, "MM/dd/yyyy H:mm");
      let prevDayString = format(prevDay, "MM/dd/yyyy H:mm");
      dates.push(prevDayString + "-" + todayString);
      today = subSeconds(prevDay, 1);
    }

    const datasets = [];

    for (let key of Object.keys(graphData)) {
      datasets.push({
        name: key,
        type: "line",
        values: graphData[key],
      });
    }

    const data = {
      labels: [...dates],
      datasets,
    };

    new Chart("#chart", {
      // or a DOM element,
      // new Chart() in case of ES6 module with above usage
      title: "Rolling Window of 24hrs",
      data: data,
      type: "axis-mixed", // or 'bar', 'line', 'scatter', 'pie', 'percentage'
      height: 450,
      colors: ["#7cd6fd", "#743ee2"],
    });
  }, [graphData]);

  return (
    <Wrapper>
      <Header>Crypto Track</Header>
      <MyChart id="chart"></MyChart>
    </Wrapper>
  );
}

const Wrapper = styled.div`
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 70px;
`;

const MyChart = styled.div``;

const Header = styled.span`
  box-sizing: border-box;
  font-size: 40px;
  text-align: left;
  font-weight: 400;
  font-family: "Inter", "Roboto", sans-serif;
  width: 100%;
  text-align: center;
  color: #46388c;
`;

export default App;
