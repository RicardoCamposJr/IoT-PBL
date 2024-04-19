import style from "../styles/Header.module.css"
import Device from "./Device"

export default function Header() {
  return(
    <div className={style.container}>
      <div className={style.logo}>
        Air Controller
      </div>
    </div>
  )
}