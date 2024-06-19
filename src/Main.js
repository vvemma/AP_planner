import React, { useEffect, useState } from 'react';
import './Main.css';

function Main() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/23") //여길 바꿔가며 시연하자!!
      .then(response => response.json()) // JSON 형식으로 변환
      .then(data => setData(data)); // 데이터 상태 업데이트
  }, []); // 빈 배열을 두번째 인자로 전달하여 한 번만 실행되도록 설정

  // 데이터가 없는 경우 로딩 메시지 표시
  if (!data) {
    return <div>로딩중...</div>;
  }

  // JSON 데이터를 문자열로 변환
  const jsonData = data.assign_table;

  // 각 key와 value를 담을 배열
  const keyValueDivs = [];

  // jsonData의 각 key에 대해 반복하여 key와 value를 div로 묶어서 keyValueDivs에 추가
  for (const key in jsonData) {
    if (jsonData.hasOwnProperty(key)) {
      const value = jsonData[key];
      keyValueDivs.push(
        <div key={key} className='date'>
          <h3>{key}</h3>
          <ul>
            {value.map((task, index) => (
              <li key={index}>{task}</li>
            ))}
          </ul>
        </div>
      );
    }
  }

  // 화면에 출력
  return (
    <div className='bodybody'>
      <h1>계획</h1>
      <div className="key-value-list">
        {keyValueDivs}
      </div>
    </div>
  );
}

export default Main;
