"""Кастомные исключения Page Object Model."""


class PageError(Exception):
    """Базовое исключение для операций со страницами."""


class ElementNotFoundError(PageError):
    """Элемент не найден на странице за отведённое время."""


class EmptyProductListError(PageError):
    """Список товаров пуст, операция невозможна."""


class ButtonDisabledError(PageError):
    """Кнопка заблокирована и не может быть нажата."""


class FormValidationError(PageError):
    """Форма не прошла валидацию."""


class LimitExceededError(PageError):
    """Превышен лимит, заданный в ТЗ."""