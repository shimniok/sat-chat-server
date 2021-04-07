angular
  .module("user.service", ["ngResource"])

  .factory("UserService", [
    "$resource",
    function ($resource) {
      return $resource("/api/user/:id", { id: "@id" });
    },
  ]);
