#generate's app
from django.urls import path, include
from .views import *

urlpatterns = [
    path('ai/', GenerateSchemeAI.as_view(), name="generate-scheme-ai"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
path(
    "projects/editor/<slug:project_slug>/",
    ProjectDetailCanvasView.as_view(),
    name="project-editor-detail"
),
path(
  "projects/runtime/<slug:project_slug>/",
  ProjectDetailPreviewView.as_view(),
),
    path('projects/<slug:project_slug>/', LiveProjectAPIView.as_view(), name='live-project-api'),

    path("projects/<int:pk>/save_all/", SaveAllView.as_view(), name="project-save-all"),
    path("test2/", test2.as_view(), name="test2"),
    path("projects/<int:project_id>/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:project_id>/pages/",ProjectPageCreateView.as_view(),),
    path('projects/<int:project_id>/pages/<int:page_id>/', PageDetailAPIView.as_view(), name='page-detail'),

    path(
        "projects/<int:project_id>/save/",
        SaveLiveAppDataView.as_view(),
        name="publish-live-appdata",
    ),
    path(
        "projects/<int:project_id>/replace-schema/",
        RenameLiveTablesAndFieldsAPIView.as_view(),
        name="replace-live-schema"
    ),
    path(
        "upload-image/<str:element_id>/",
        ImageUploadView.as_view(),
        name="upload_image"
    ),
path('reactjs/', reactjs.as_view(), name="reactjs")
    # path('code/model/', GenerateModelJsonSchemeAPIView.as_view()),
    # path("apps/", GeneratedAppListView.as_view(), name="list-apps"),
    # path("apps/<int:pk>/", GeneratedAppDetailView.as_view(), name="get-app"),
    # path("apps/<int:pk>/update/", GeneratedAppUpdateView.as_view(), name="update-app"),
    # path("apps/<int:app_id>/rollback/<int:version_id>/", RollbackAppView.as_view(), name="rollback-app"),

]
