from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        """
        Return a list of tags to be applied to the operation.

        It is possible to override the tags by setting the `api_tags` attribute
        """
        tags = self.overrides.get("tags", None) or getattr(self.view, "api_tags", [])
        if not tags:
            tags = [operation_keys[0]]

        return tags

    def get_operation_id(self, operation_keys=None):
        """
        Return operation ID.

        It is possible to override the operation ID by setting the `api_operation_id` attribute
        """

        operation_id = self.overrides.get("operation_id", None) or getattr(
            self.view, "api_operation_id", None
        )
        if not operation_id:
            operation_id = "_".join(operation_keys)

        return operation_id

    # def get_summary_and_description(self):
    #     summary = self.overrides.get("operation_summary", None) or getattr(
    #         self.view, "api_summary", None
    #     )
    #     description = self.overrides.get("operation_description", None) or getattr(
    #         self.view, "api_description", None
    #     )
