import style from "../styles/Device.module.css"
import { TbAirConditioningDisabled } from "react-icons/tb";
import { FaTemperatureEmpty } from "react-icons/fa6";
import { IoIosGitNetwork } from "react-icons/io";
import { FaPowerOff } from "react-icons/fa";
import { FaExchangeAlt } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { useEffect, useState } from "react";
import brokerIP from './../broker'

export default function Device({name, temp, status, IPPORT, time}) {

  const [clicked, setClicked] = useState(false)
  const [changeTemp, setChangeTemp] = useState()
  const [change, setChange] = useState(false)
  const [clickedDelete, setClickedDelete] = useState(false)

  useEffect(() => {
    if (clicked) {
      // Função para fazer a requisição
      const fetchData = async () => {
        try {
          await fetch(`http://${brokerIP}:8082/power/${IPPORT[0]}/`, {
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
      setClicked(false)
    }
  }, [clicked]);

  const handleClick = () => {
    if (clicked === true) {
      console.log("mudou")
      setClicked(false)
    } else if (clicked === false) {
      console.log("mudou")
      setClicked(true)
    }
  };

  useEffect(() => {
    if (clickedDelete) {
      // Função para fazer a requisição
      const fetchData = async () => {
        try {
          await fetch(`http://${brokerIP}:8082/delete/${IPPORT[0]}/`, {
            method: 'DELETE',
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
      setClickedDelete(false)
    }
  }, [clickedDelete]);

  const handleClickDelete = () => {
    if (clickedDelete === true) {
      setClickedDelete(false)
    } else if (clickedDelete === false) {
      setClickedDelete(true)
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
        await fetch(`http://${brokerIP}:8082/set/${IPPORT[0]}/${changeTemp}`, {
          method: 'POST',
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
    <div className={style.card}>
    {/* Div das info */}
      <div className={style.container}>

        <div className={style.total}>
          {/* Div do power */}
          <div className={style.power}>
          {status ? (
              <FaPowerOff onClick={handleClick} className={style.powerONIcon}/>
            ): 
              <FaPowerOff onClick={handleClick} className={style.powerOFFIcon}/>
            }
          </div>

          <div className={style.rightData}>

            {/* Div do nome */}
            <div className={style.info}>
              <TbAirConditioningDisabled className={style.icon}/>
              <span>{name}</span>
            </div>

            {/* Div do IP */}
            <div className={style.info}>
              <IoIosGitNetwork className={style.iconIP}/>
              <span>{IPPORT[0]}</span>
            </div>
          </div>

        </div>

        <div className={style.change}>
          <FaExchangeAlt className={style.iconChange} onClick={openModal}/>
        </div>
        <div>
          <MdDelete className={style.iconChange} onClick={handleClickDelete}/>
        </div>
      </div>

      {/* Div da temperatura */}
      <div className={style.tempContainer}>
        {status ? (
          <>
            <FaTemperatureEmpty className={style.icontemp}/>
            <div className={style.temperature}>{temp}°C</div>
          </>
        ): (
          <>
            <FaTemperatureEmpty className={style.icontemp}/>
            <div className={style.temperatureNot}>{temp}</div>
          </>
        )}
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
    </div>
  )
}