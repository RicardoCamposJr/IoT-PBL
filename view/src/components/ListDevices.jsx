import style from "../styles/ListDevices.module.css"
import Device from "./Device"

export default function ListDevices({listDevices}) {
  console.log(listDevices)
  return(
    <div className={style.container}>
      <h2>Dispositivos disponíveis</h2>
      <ul>
      {listDevices ? (
        listDevices.map((device) => (
          <li>
          <Device 
            key={device.chave}
            IPPORT={device.IPPORT}
            name={device.deviceName}
            temp={device.message}
            status={device.status}
            time={device.time}
          />
          </li>
        ))
      ): null}
      </ul>
    </div>
  )
}