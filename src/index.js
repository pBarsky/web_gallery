function main() {
	const ll = new LazyLoad();

	const showHideButton = document.getElementById('show-button');
	const sizeButton = document.getElementById('change-size-button');
	const files = document.querySelector('.files');
	const wrappers = document.querySelectorAll('.wrapper');
	const images = document.querySelectorAll('img');
	const sources = document.querySelectorAll('source');

	showHideButton.addEventListener('click', () => {
		files.classList.toggle('hidden');
		showHideButton.classList.toggle('active-button');
	});

	sizeButton.addEventListener('click', () => {
		sizeButton.classList.toggle('active-button');
		const toggleMaxHeightClass = ({ classList }) =>
			classList.toggle('no-max-height');
		wrappers.forEach(toggleMaxHeightClass);
		images.forEach(toggleMaxHeightClass);
		sources.forEach(({ parentNode }) => toggleMaxHeightClass(parentNode));
	});

	images.forEach((el) => {
		el.addEventListener('click', () => window.open(el.src, '_blank'));
	});

	sources.forEach(({ parentNode, attributes }) => {
		parentNode?.addEventListener('click', (event) => {
			event.preventDefault();
			const target = event.target;
			if (!target.paused) {
				target.pause();
			}
			window.open(attributes[0].value, '_blank');
		});
	});
}

window.addEventListener('load', main);
