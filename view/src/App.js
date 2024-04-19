import { useEffect, useState } from 'react';
import './App.css';
import Header from './components/Header';
import ListDevices from './components/ListDevices';


function App() {
  const [devices, setDevices] = useState([])

  useEffect(() => {
    // Função para fazer a requisição
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8082/devices');
        const data = await response.json();
        const listaDeObjetos = Object.entries(data).map(([chave, valor]) => ({ chave, ...valor }));
        // console.log(listaDeObjetos)
        setDevices(listaDeObjetos);
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
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
      <ListDevices listDevices={devices}/>
    </div>
    
  );
}

export default App;
