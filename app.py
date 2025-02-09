import gradio as gr

from controllers import check_login
from controllers import check_md as check_md_controllers
from controllers import convert_from_md_to_pdf as convert_from_md_to_pdf_controller
from controllers import get_md as get_md_controller
from controllers import get_reference_file_names as get_reference_file_names_controller
from controllers import get_video_names as get_video_names_controller
from controllers import upload_reference_files as upload_reference_files_controller
from controllers import upload_videos as upload_videos_controller
from image import svg_text
from views import style

# 変数
## TODO: 本番用に書き換え
reference_file_dir_path = "assets/tmp/reference-file"
video_dir_path = "assets/tmp/video"

# アプリ
with gr.Blocks(
    css=style.custom_css,
    title="Presio",
    theme=gr.themes.Default(
        primary_hue=gr.themes.Color(
            name="customblue",
            c50="#f0f8ff",
            c100="#d9edff",
            c200="#b3daff",
            c300="#8fc7ff",
            c400="#67b4ff",
            c500="#408FF0",
            c600="#3a80d9",
            c700="#346dc4",
            c800="#2e5b9f",
            c900="#28477a",
            c950="#1b2f4d",
        )
    ),
) as demo:
    ## プロジェクト情報
    project_info = gr.State()
    ## UI
    gr.HTML(f"""
    <div style="text-align: center;">
        {svg_text.header_logo}
    </div>
    """)
    ### ログイン
    with gr.Group(elem_id="group_login", visible=True) as group_login:
        with gr.Column():
            textbox_project_name = gr.Textbox(label="プロジェクト名")
            textbox_password = gr.Textbox(
                label="パスワード",
                type="password",
            )
            button_login = gr.Button(value="ログイン", variant="primary")
    markdown_login_msg = gr.Markdown(
        elem_id="markdown_login_msg",
        value="新規プロジェクトの場合は新しいプロジェクトIDとパスワードを入力してください。<br>既存プロジェクトがある場合は既存のプロジェクトIDとパスワードを入力してください。",
        visible=True,
    )
    ### ファイル関連アップロードエリア
    with gr.Row(elem_classes=["input-row"], visible=False) as row_app_ui:
        with gr.Column(elem_classes=["file-input-column"]):
            with gr.Row(elem_classes=["file-input-row"]):
                #### HTMLコンポーネント（左側） - 1:2の比率
                with gr.Column(scale=1, min_width=150):
                    gr.HTML(f"""
                    <div style="height:100%; display: flex; justify-content: center; align-items: center;">
                        {svg_text.file_up}
                    </div>
                    """)

                #### gr.Filesコンポーネント（右側） - 1:2の比率
                with gr.Column(scale=2, min_width=300):
                    upload_reference_files = gr.Files(
                        label="参照ファイルのアップロード",
                        type="filepath",
                        height=130,
                        elem_id="upload_reference_files",
                        file_types=[".pdf", ".PDF"],
                    )
            select_reference_files = gr.Dropdown(
                label="参照ファイルの選択",
                multiselect=True,
                interactive=True,
                elem_id="select_reference_files",
                choices=[],
                value=None,
            )
        with gr.Column():
            with gr.Row(elem_classes=["file-input-row"]):
                #### HTMLコンポーネント（左側） - 1:2の比率
                with gr.Column(scale=1, min_width=150):
                    gr.HTML(f"""
                    <div style="height:100%; display: flex; justify-content: center; align-items: center;">
                        {svg_text.video_up}
                    </div>
                    """)

                #### gr.Filesコンポーネント（右側） - 1:2の比率
                with gr.Column(scale=2, min_width=300):
                    upload_video = gr.Video(
                        label="ビデオのアップロード",
                        sources=["upload"],
                        height=130,
                        elem_id="upload_video",
                    )
            select_video = gr.Dropdown(
                label="ビデオの選択",
                multiselect=False,
                interactive=True,
                elem_id="select_video",
                choices=[],
                value=None,
            )
    ### MarkDownエリア
    with gr.Row(visible=False) as row_output:
        with gr.Column():
            with gr.Tab(label="Markdown") as tab_markdown:
                edit_markdown = gr.Code(
                    show_label=False,
                    language="markdown",
                    wrap_lines=True,
                    elem_id="edit_markdown",
                )
        with gr.Column():
            with gr.Tab(label="Markdown", elem_id="tab_output") as tab_output:
                output_markdown = gr.Markdown(
                    show_label=False, container=True, elem_id="output_markdown"
                )
            with gr.Tab(label="スライド", elem_id="tab_output") as tab_output:
                output_slide = gr.HTML(
                    show_label=False, container=True, elem_id="output_slide"
                )

    ## イベント処理
    ### ログインボタンクリック時、ログイン処理
    button_login.click(
        fn=check_login.exec,
        inputs=[textbox_project_name, textbox_password],
        outputs=project_info,
    )
    project_info.change(fn=lambda: gr.Group(visible=False), outputs=[group_login])
    project_info.change(
        fn=lambda: gr.Markdown(visible=False), outputs=[markdown_login_msg]
    )
    project_info.change(fn=lambda: gr.Group(visible=True), outputs=[row_app_ui])
    project_info.change(fn=lambda: gr.Row(visible=True), outputs=[row_output])
    project_info.change(
        fn=get_reference_file_names_controller.exec,
        inputs=[project_info],
        outputs=[select_reference_files],
    )
    project_info.change(
        fn=get_video_names_controller.exec,
        inputs=[project_info],
        outputs=[select_video],
    )
    ### 参照ファイルアップロード
    upload_reference_files.upload(
        fn=upload_reference_files_controller.exec,
        inputs=[upload_reference_files, select_reference_files, project_info],
        outputs=[select_reference_files],
    )
    ### 参照ファイル選択時に選択肢更新
    select_reference_files.focus(
        fn=get_reference_file_names_controller.exec,
        inputs=[project_info],
        outputs=[select_reference_files],
    )
    ### 参照ファイル選択後、Markdown更新
    select_reference_files.change(
        fn=get_md_controller.exec,
        inputs=[project_info, select_reference_files, select_video],
        outputs=[edit_markdown],
    )
    ### 動画アップロード
    upload_video.upload(
        fn=upload_videos_controller.exec,
        inputs=[upload_video, project_info],
        outputs=[select_video],
    )
    ### 動画選択時に値初期化
    select_video.focus(
        fn=lambda: gr.Dropdown(value=None),
        outputs=[select_video],
    )
    ### 動画選択時に選択肢更新
    select_video.focus(
        fn=get_video_names_controller.exec,
        inputs=[project_info],
        outputs=[select_video],
    )
    ### 動画選択選択後、Markdown表示
    select_video.change(
        fn=get_md_controller.exec,
        inputs=[project_info, select_reference_files, select_video],
        outputs=[edit_markdown],
    )
    ### Markdownを更新後、生成資料（Markdown）を更新
    edit_markdown.change(
        fn=lambda text: text, inputs=[edit_markdown], outputs=[output_markdown]
    )
    ### Markdownを更新後、生成資料（スライド）を更新
    edit_markdown.change(
        fn=convert_from_md_to_pdf_controller.exec,
        inputs=[edit_markdown],
        outputs=[output_slide],
    )
    ### Markdownを更新後、firebaseのmarkdownsコレクションを更新
    edit_markdown.change(
        fn=check_md_controllers.exec,
        inputs=[project_info, select_reference_files, select_video, edit_markdown],
        outputs=[output_slide],
    )

# アプリ起動
if __name__ == "__main__":
    demo.launch(
        favicon_path="image/favicon/favicon.png",
        show_api=False,
    )
