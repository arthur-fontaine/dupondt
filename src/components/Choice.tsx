import './../style/choice.scss';
import './../style/tag.scss';

function Choice({
	choice,
	selected = false,
	incoming = false
}: {
	choice: string;
	selected?: boolean;
	incoming?: boolean;
}) {
	return (
		<div className={`choice ${selected ? 'choice--selected' : ''}`}>
			<p>{choice}</p>
			{incoming && <div className="tag tag--incoming">incoming</div>}
		</div>
	);
}

export default Choice;
