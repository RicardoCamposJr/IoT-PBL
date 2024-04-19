import style from "../styles/ListDevices.module.css"
import Device from "./Device"

export default function ListDevices({listDevices}) {
  console.log(listDevices)
  return(
    <div className={style.container}>
      {listDevices ? (
        listDevices.map((device) => (
          <Device 
            key={device.chave}
            IPPORT={device.IPPORT}
            name={device.deviceName}
            temp={device.message}
            status={device.status}
            time={device.time}
          />
        ))
      ): null}
    </div>
  )
}