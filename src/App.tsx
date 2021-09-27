import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Footer from './components/Footer';
import Header from './components/Header';
import Home from './routes/Home';
import FindThePath from './routes/Simulation/FindThePath';
import './style/style.scss';

function App() {
	return (
		<div className="app">
			<Router>
				<Header />
				<Switch>
					{/* <Route path="/world" component={GeneratePopulation} /> */}
					<Route path="/simulation/find-path" component={FindThePath} />
					<Route path="/" component={Home} />
				</Switch>
				<Footer />
			</Router>
		</div>
	);
}

export default App;
