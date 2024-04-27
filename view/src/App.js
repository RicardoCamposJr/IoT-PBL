import { useEffect, useState } from 'react';
import './App.css';
import Header from './components/Header';
import ListDevices from './components/ListDevices';
import brokerIP from './broker'


function App() {
  const [devices, setDevices] = useState([])
  const [serverStatus, setServerStatus] = useState(false)

  useEffect(() => {
    // Função para fazer a requisição
    const fetchData = async () => {
      try {
        const response = await fetch(`http://${brokerIP}:8082/devices`);
        const data = await response.json();
        const listaDeObjetos = Object.entries(data).map(([chave, valor]) => ({ chave, ...valor }));
        setServerStatus(true)
        setDevices(listaDeObjetos);
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
        setServerStatus(false)
      }
    };

    // Chama a função de busca de dados quando o componente monta
    fetchData();

    const interval = setInterval(fetchData, 2000)

    return () => clearInterval(interval)
  }, []);

  return (
    <div className="App">
      <Header />
      {serverStatus ? (
        <ListDevices listDevices={devices}/>
      ): 
      <div className='server-off'>
        Servidor desconectado!
      </div>}
    </div>
    
  );
}

export default App;
