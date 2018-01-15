import React, { Component } from 'react'
import { Col, ProgressBar } from 'react-materialize'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'


const mapStateToProps = (state) => {
	return {
		...state,
	}
}


class ProgressBarLoader extends Component {

	static propTypes = {
		pending: PropTypes.bool.isRequired,
		fulfilled: PropTypes.bool.isRequired,
		error: PropTypes.bool.isRequired
	}

	render() {
		let color
		if(this.props.pending) {
			color = 'yellow'
		} 
		
		else if(this.props.fulfilled) {
			color = 'green'
		} 
		
		else if (this.props.error) {
			color = 'red'
		}

		const shouldRender = !!color

		const classList = `loader ${color}`
		return shouldRender ? (
			<Col s={12}>
				<ProgressBar className={classList} />
			</Col>
		) : null
	}

}


export default connect(mapStateToProps)(ProgressBarLoader)

