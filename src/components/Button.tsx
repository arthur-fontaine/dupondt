import './../style/button.scss';

function Button({
	value,
	onClick
}: {
	value: string;
	onClick: React.MouseEventHandler<HTMLDivElement>;
}) {
	return (
		<div className="button" onClick={onClick}>
			{value}
		</div>
	);
}

export default Button;
