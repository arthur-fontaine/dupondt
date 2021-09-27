import './../style/header.scss';
import GithubLogo from './../assets/images/github-fill.svg';
import { useHistory } from 'react-router-dom';

function Header() {
	const history = useHistory();

	const goToHome = () => history.push('/');

	return (
		<header>
			<div className="title">
				<h1 onClick={goToHome}>Dupondt</h1>
				<h4>Exploitation of the theory of the six degrees of separation.</h4>
			</div>
			<a href="https://github.com/arthur-fontaine/dupondt" target="_blank">
				<img src={GithubLogo} alt="Github Logo" className="github-logo" />
			</a>
		</header>
	);
}

export default Header;
