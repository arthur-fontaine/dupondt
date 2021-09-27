import Choice from './Choice';
import './../style/choice-bar.scss';

function ChoiceBar({
	choices
}: {
	choices: { [choice: string]: { selected?: boolean; incoming?: boolean } };
}) {
	return (
		<div className="choice-bar">
			{Object.entries(choices).map((choice) => (
				<Choice
					key={choice[0]}
					choice={choice[0]}
					selected={choice[1].selected}
					incoming={choice[1].incoming}
				/>
			))}
		</div>
	);
}

export default ChoiceBar;
