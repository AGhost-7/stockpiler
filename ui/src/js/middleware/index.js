import { applyMiddleware } from 'redux'
import { createLogger } from 'redux-logger'

const middleware = applyMiddleware(
	createLogger()
)

export default middleware
