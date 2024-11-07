from dishka import Provider, provide

from src.domain.user.usecase.user import CreateUserService, AuthorizationService, UserProfileService


class ServiceProvider(Provider):
    user_service = provide(CreateUserService)
    auth_service = provide(AuthorizationService)
    profile_service = provide(UserProfileService)
