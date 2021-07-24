import glob
import importlib
import inspect
from pathlib import Path

from flask import Flask

from flask_next.HTMLView import HTMLView


class DynamicSetup:
    modules: dict = {}
    secure_routes = {}
    public_routes = {}
    route_count: int = 0
    allowable_methods = ["GET", "PUT", "POST", "DELETE"]

    def __init__(self, _app: Flask = None):
        self.app = _app

    def get_methods(self, method_parts):
        methods = []
        secure = False
        for index, method in enumerate(method_parts):
            method = method.upper()
            if method in self.allowable_methods:
                methods.append(method)
            elif method == "SECURE":
                secure = True
            else:
                return methods, index, secure
        return methods, 0, secure

    def add_route(self, route_path: Path, base_url):
        module_name = ".".join(route_path.parts)[0:-3]
        self.modules[route_path] = importlib.import_module(module_name)
        for method_name in dir(self.modules[route_path]):
            rule_url = None
            secure = False
            if not method_name.startswith("_"):
                methods = ["GET"]
                method_parts = method_name.split("_")
                if method_parts[0] == "index":
                    rule_url = base_url
                else:
                    if len(method_parts) > 1:
                        methods, method_start, secure = self.get_methods(method_parts)
                        if methods:
                            end_point_method = "_".join(method_parts[method_start:])
                            rule_url = f"/{base_url}/{end_point_method}"

                        # any route under /routes/secure become secure
                        if route_path.parts[1] == "secure":
                            secure = True
                if rule_url:
                    view_func = getattr(self.modules[route_path], method_name)
                    sig = inspect.signature(view_func)
                    for param in sig.parameters.values():
                        param_type = ""
                        if param.annotation is not inspect.Parameter.empty:
                            if param.annotation is int:
                                param_type = "int:"
                            elif param.annotation is float:
                                param_type = "float:"
                            else:
                                self.app.logger.warning(
                                    f"{method_name}: unknown parameter type: {param.annotation}"
                                )
                        rule_url += f"/<{param_type}{param.name}>"

                    self.app.logger.info(
                        f"{method_name}: add_url_rule: {rule_url} {methods}"
                    )
                    endpoint = f"{module_name}.{method_name}"
                    self.app.add_url_rule(
                        rule_url,
                        view_func=view_func,
                        endpoint=endpoint,
                        methods=methods,
                    )
                    if secure:
                        self.secure_routes[endpoint] = rule_url
                    else:
                        self.public_routes[endpoint] = rule_url
                    self.route_count += 1

    def add_html(self, route_path: Path, rule_url: str):
        endpoint = ".".join(route_path.parts)
        self.app.add_url_rule(
            rule_url,
            view_func=HTMLView.as_view(endpoint, route_path),
            endpoint=endpoint,
        )
        self.route_count += 1

        if route_path.parts[1] == "secure":
            self.secure_routes[endpoint] = rule_url
        else:
            self.public_routes[endpoint] = rule_url

    def spelunk(self):
        for d in glob.glob("./routes/**/[!_]*", recursive=True):
            route_path = Path(d)
            suffix = route_path.suffix.lower()
            if route_path.is_file() and suffix in [".html", ".py"]:
                base_url = "/".join(route_path.parts[1:-1])
                if route_path.stem != "index":
                    base_url += f"/{route_path.stem}"
                base_url = "/" + base_url

                if suffix == ".py":
                    # api or flask routes
                    self.add_route(route_path, base_url)

                if suffix == ".html":
                    # static serve HTML
                    self.add_html(route_path, base_url)

        return self.route_count

    def print(self):
        """
        display current routes, secure routes and modules
        """
        self.app.logger.info(self.modules.keys())
        self.app.logger.info(self.app.url_map)
        self.app.logger.info(self.secure_routes)
