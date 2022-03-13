import logo from './logo.svg';
import './App.css'; 
import TransactionManage from './components/transactionManage';
import './css/desing.css'
function App() {
  const url = "http://localhost:5000/";

  return (
    <div>
      <TransactionManage url={url}></TransactionManage>   
    </div>
  );
}

export default App;
