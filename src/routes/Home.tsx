import './../style/home.scss';
import './../style/field.scss';
import { useHistory } from 'react-router';
import ChoiceBar from '../components/ChoiceBar';
import { SyntheticEvent } from 'react';
import Button from '../components/Button';
import { simulation } from '../utils/dupondt';

function Home() {
	let numberInhabitants: number = 5000;
	const history = useHistory();

	return (
		<div className="home">
			<ChoiceBar
				choices={{
					simulation: { selected: true },
					instagram: { incoming: true },
					// instagram: { incoming: true },
					mastodon: { incoming: true }
				}}
			/>
			<div>
				<div className="population-field">
					<p>Population:</p>
					<input
						defaultValue={numberInhabitants}
						min="100"
						max="9999999"
						step="100"
						type="number"
						className="field"
						onChange={(e: SyntheticEvent) => {
							const inputElement = e.target as HTMLInputElement;
							const value = inputElement.valueAsNumber;
							if (value < parseFloat(inputElement.min))
								inputElement.value = inputElement.min;
							else if (value > parseFloat(inputElement.max))
								inputElement.value = inputElement.max;
							numberInhabitants = parseFloat(inputElement.value);
						}}
					/>
				</div>
				<Button
					value="Generate"
					onClick={async (e) => {
						const element = e.target as HTMLDivElement;
						const initialInnerText = element.innerText;
						element.innerText = 'Loading...';
						setTimeout(async () => {
							const { following, followers, accounts } = await simulation.build(
								numberInhabitants
							);
							element.innerText = initialInnerText;
							history.push({
								pathname: '/simulation/find-path',
								state: { following, followers, accounts }
							});
						}, 0);
					}}
				/>
			</div>
		</div>
	);
}

export default Home;
