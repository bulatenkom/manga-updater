import { RouteRecordRaw } from 'vue-router';

export function prefixRoutes(prefix: string, routes: Array<RouteRecordRaw>) {
  return routes.map((route) => (route.path = prefix + '/' + route.path));
}

export function toObject(list: unknown[] | null) {
  if (list) {
    const res: Record<string, unknown> = {};
    list.forEach((el) => {
      res[el.uuid] = el;
    });
    return res;
  }
  return null;
}
