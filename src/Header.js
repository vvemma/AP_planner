import React from "react";
import "./Header.css"

const Header = () => {
    return (
      <header className="header">
        <div className="contents">
          <div>
            인곽인들을 위한 플래너
          </div>
  
          <nav className="navigation">
            <ul>
              <li>
                {/* 메뉴1 */}
                made by 이정민
              </li>
              <li>
                {/* 메뉴2 */}
              </li>
            </ul>
          </nav>
        </div>
      </header>
    )
  }
  
  export default Header