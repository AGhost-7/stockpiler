import React from 'react';
import ReactDOM from 'react-dom';
import App from '../App';
import registerServiceWorker from '../services/registerServiceWorker';
import { Chrome } from 'navalia';

const assert = console.assert;
const baseUrl = 'http://localhost:3000';

describe('E2E Testing', () => {

	let chrome = {};

	beforeEach(() => {
		chrome = new Chrome();
	});

	it('renders without crashing', () => {
		const div = document.createElement('div');
		ReactDOM.render(<App />, div);
		registerServiceWorker();
	});

	it('loads the homepage and verifys the title', () => {
		loadPageAndVerifyTitle(chrome, baseUrl, 'Stockpiler');
	});

});

// Helper functions
// @todo: move in class
async function loadPageAndVerifyTitle(chrome = false, url = '', title = '') {
	await chrome.goto(url);
	const result = await chrome.html('title');
	assert(result, `<title>${title}</title>`);
	return chrome.done();
}

