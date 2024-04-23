import style from "../styles/Header.module.css"
import Device from "./Device"

export default function Header() {
  return(
    <div className={style.container}>
      <div className={style.logo}>
        Controlador de dispositivos
      </div>
    </div>
  )
}