angular
  .module("rockblock.service", ["ngResource"])

  .factory("RockBlockProvider", [
    "$resource",
    function ($resource) {
      return $resource(
        "/api/send",
        {},
        {
          send: { method: "post" },
        }
      );
    },
  ]);
