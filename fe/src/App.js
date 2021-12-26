import logo from "./logo.svg";
import "./App.css";
import { Chart } from "frappe-charts/dist/frappe-charts.min.esm";

import styled from "styled-components";
import { useEffect } from "react";

function App() {
  useEffect(() => {
    const data = {
      labels: [
        "12am-3am",
        "3am-6pm",
        "6am-9am",
        "9am-12am",
        "12pm-3pm",
        "3pm-6pm",
        "6pm-9pm",
        "9am-12am",
      ],
      datasets: [
        {
          name: "Some Data",
          type: "bar",
          values: [25, 40, 30, 35, 8, 52, 17, -4],
        },
        {
          name: "Another Set",
          type: "line",
          values: [25, 50, -10, 15, 18, 32, 27, 14],
        },
      ],
    };

    new Chart("#chart", {
      // or a DOM element,
      // new Chart() in case of ES6 module with above usage
      title: "Crypto mentions in the past",
      data: data,
      type: "axis-mixed", // or 'bar', 'line', 'scatter', 'pie', 'percentage'
      height: 450,
      colors: ["#7cd6fd", "#743ee2"],
    });
  });

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
`;

export default App;
