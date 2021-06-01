import './App.css';

import { Router, Route, Switch } from "react-router-dom";
import { createBrowserHistory } from "history";
import Globals from "./styles/Globals"
import Auth from "./pages/Auth";

const history = createBrowserHistory();

function App() {
  return (
    <Router history={history}>
    <Globals />
    <Switch>
      <Route exact path="/" component={Auth} />
      {/* <Route exact path="/" component={HomePage} /> */}
      {/* <Route exact path="/projects" component={ProjectsPage} /> */}
      {/* <Route exact path="/about" component={AboutPage} /> */}
      {/* <Route exact path="/bookshelf" component={BookPage} /> */}
      {/* <Route component={NotFound} /> */}
    </Switch>
  </Router>
  );
}

export default App;
