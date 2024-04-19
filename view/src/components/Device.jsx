import style from "../styles/Device.module.css"
import { TbAirConditioningDisabled } from "react-icons/tb";
import { FaTemperatureEmpty } from "react-icons/fa6";
import { IoIosGitNetwork } from "react-icons/io";
import { FaPowerOff } from "react-icons/fa";
import { FaExchangeAlt } from "react-icons/fa";
import { useEffect, useState } from "react";

export default function Device({name, temp, status, IPPORT, time}) {

  const [clicked, setClicked] = useState(false)
  const [changeTemp, setChangeTemp] = useState()
  const [change, setChange] = useState(false)

  useEffect(() => {
    if (clicked) {
      // Função para fazer a requisição
      const fetchData = async () => {
        try {
          await fetch(`http://localhost:8082/power/${IPPORT[0]}/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
          });
        } catch (error) {
          console.error('Erro ao buscar dados:', error);
        }
      };

      fetchData()
    }
  }, [clicked]);

  const handleClick = () => {
    if (clicked === true) {
      setClicked(false)
    } else if (clicked === false) {
      setClicked(true)
    }
  };

  const [modalOpen, setModalOpen] = useState(false);

  const openModal = () => {
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);

    if (change === true) {
      setChange(false)
    } else if (change === false) {
      setChange(true)
    }
  };

  const handleChange = (event) => {
    setChangeTemp(event.target.value);
    console.log(changeTemp)
  };

  useEffect(() => {
    
    const fetchData = async () => {
      try {
        await fetch(`http://localhost:8082/set/${IPPORT[0]}/${changeTemp}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({}),
        });
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      }
    };

    fetchData()
  }, [change]);

  return(
    <>
      <div className={style.container}>
        <div className={style.data}>
          <TbAirConditioningDisabled className={style.icon}/>
          <div>{name}</div>
          {status ? (
            <>
              <FaTemperatureEmpty className={style.icontemp}/>
              <div>{temp}°C</div>
            </>
          ): (
            <>
              <FaTemperatureEmpty className={style.icontemp}/>
              <div>{temp}</div>
            </>
          )}
          <IoIosGitNetwork className={style.icontemp}/>
          <div>{IPPORT[0]}</div>
        </div>
        <div>
          <FaExchangeAlt className={style.iconChange} onClick={openModal}/>
        </div>
        <div>
          {status ? (
            <FaPowerOff onClick={handleClick} className={style.powerONIcon}/>
          ): 
            <FaPowerOff onClick={handleClick} className={style.powerOFFIcon}/>
          }
        </div>
      </div>
      {modalOpen && (
          <div className={style.containerSet} onClick={closeModal}>
            <div className={style.modalContent} onClick={(e) => e.stopPropagation()}>
              <FaTemperatureEmpty className={style.icontemp}/>
              <p>Mude a temperatura</p>
              <input type="text"  onChange={handleChange} />
              <button className={style.modalBtn} onClick={closeModal}>Enviar</button>
            </div>
          </div>
        )}
    </>
  )
}